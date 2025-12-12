from libifstate.util import get_netns_run_dir, dump_yaml_file, slurp_yaml_file, RUN_BASE_DIR
from libifstate.util import logger

import logging
from pathlib import Path
import os
import pkgutil
from shlex import quote
import shutil
from string import Template
import subprocess
import tempfile


HOOK_DIR = '/etc/ifstate/hooks'
HOOK_WRAPPER = Template(pkgutil.get_data("libifstate", "hook/wrapper.sh").decode("utf-8"))

RC_OK = 0
RC_ERROR = 1
RC_STARTED = 2
# it is the same value, but there are two constants to make it more convinient
RC_STOPPED = RC_STARTED
RC_CHANGED = 3

def _open_perm(path, flags):
    return os.open(path, flags, 0o600)

class Hook():
    def __init__(self, name, script, provides=[], after=[]):
        self.name = name

        if script[0] == '/':
            self.script = Path(script).as_posix()
        else:
            self.script = Path(HOOK_DIR, script).as_posix()

        self.provides = provides
        self.after = after

    def start(self, link, args, run_dir, do_apply):
        wrapper_fn = f"{run_dir}/wrapper.sh"

        with open(wrapper_fn, "w", opener=_open_perm) as fh:
            template_vars = {
                    'verbose': 1 if logger.getEffectiveLevel() == logging.DEBUG else '',
                    'script': self.script,
                    'ifname': link.settings.get('ifname'),
                    'index': link.idx,
                    'netns': link.netns.netns or '',
                    'vrf': '',
                    'rundir': run_dir,
                    'rc_ok': RC_OK,
                    'rc_error': RC_ERROR,
                    'rc_started': RC_STARTED,
                    'rc_stopped': RC_STOPPED,
                    'rc_changed': RC_CHANGED,
                }

            if link.get_if_attr('IFLA_INFO_SLAVE_KIND') == 'vrf':
                template_vars['vrf'] = link.settings.get('master')

            args_list = []
            for k, v in args.items():
                args_list.append(f'export IFS_ARG_{k.upper()}={quote(v)}')
            template_vars['args'] = "\n".join(args_list)

            try:
                fh.write(HOOK_WRAPPER.substitute(template_vars))
            except KeyError as ex:
                logger.error("Failed to prepare wrapper for hook {}: variable {} unknown".format(self.name, str(ex)))
                return
            except ValueError as ex:
                logger.error("Failed to prepare wrapper for hook {}: {}".format(self.name, str(ex)))
                return

        try:
            if do_apply:
                subprocess.run(['/bin/sh', wrapper_fn, "start"], timeout=3, check=True)
            else:
                subprocess.run(['/bin/sh', wrapper_fn, "check-start"], timeout=3, check=True)

            return RC_OK
        except (FileNotFoundError, PermissionError) as ex:
            logger.error("Failed executing hook {}: {}".format(self.name, str(ex)))
            return RC_ERROR
        except subprocess.TimeoutExpired as ex:
            logger.error("Running hook {} has timed out.".format(self.name))
            return RC_ERROR
        except subprocess.CalledProcessError as ex:
            if ex.returncode < 0:
                logger.warning("Hook {} got signal {}".format(hook_name, -1 * ex.returncode))
                return RC_ERROR

            return ex.returncode

    @staticmethod
    def stop(link, hook_name, run_dir, do_apply):
        wrapper_fn = f"{run_dir}/wrapper.sh"

        try:
            if do_apply:
                subprocess.run(['/bin/sh', wrapper_fn, "stop"], timeout=3, check=True)
            else:
                subprocess.run(['/bin/sh', wrapper_fn, "check-stop"], timeout=3, check=True)

            return RC_OK
        except (FileNotFoundError, PermissionError) as ex:
            logger.error("Failed executing hook {}: {}".format(hook_name, str(ex)))
            return RC_ERROR
        except subprocess.TimeoutExpired as ex:
            logger.error("Running hook {} has timed out.".format(hook_name))
            return RC_ERROR
        except subprocess.CalledProcessError as ex:
            if ex.returncode < 0:
                logger.warning("Hook {} got signal {}".format(hook_name, -1 * ex.returncode))
                return RC_ERROR

            assert(run_dir.startswith(RUN_BASE_DIR))

            try:
                shutil.rmtree(run_dir)
            except FileNotFoundError:
                pass
            except OSError as err:
                logger.error("Failed cleanup hook rundir {}: {}".format(run_dir, str(err)))

            return ex.returncode

class Hooks():
    def __init__(self, ifstate):
        self.hooks = {}
        for hook, opts in ifstate.items():
            if 'script' in opts:
                self.hooks[hook] = Hook(hook, **opts)
            else:
                self.hooks[hook] = Hook(hook, script=hook, **opts)

    def apply(self, link, do_apply):
        run_dir = get_netns_run_dir('hooks', link.netns, str(link.idx))

        state_fn = f"{run_dir}/state"
        old_state = slurp_yaml_file(state_fn, default=[])
        run_state = []

        # Stop any running hooks which should not run any more or have other
        # parameters - hooks are identified by all of their settings. Keep
        # the rundir for any hook already running.
        for entry in old_state:
            if not entry.get('hook') in link.hooks:
                rc = Hook.stop(link, entry["hook"]["name"], entry["rundir"], do_apply)
                if rc == RC_OK:
                    pass
                elif rc == RC_STOPPED:
                    logger.log_del('hooks', '- {}'.format(entry["hook"]["name"]))
                else:
                    run_state.append(entry)
                    logger.log_err('hooks', '! {}'.format(entry["hook"]["name"]))
            else:
                hook = next((hook for hook in link.hooks if hook == entry["hook"]), None)
                # tepmorary keep mapping between running and configured hook dict
                hook["__rundir"] = entry["rundir"]

        try:
            if not link.hooks:
                return

            for hook in link.hooks:
                if not hook["name"] in self.hooks:
                    logger.warning("Hook {} for {} is unknown!".format(link.settings.get('ifname'), hook))
                    continue

                hook_run_dir = hook.get("__rundir")
                # hook is not running, yet
                if hook_run_dir is None:
                    hook_run_dir = tempfile.mkdtemp(prefix="hook_", dir=run_dir)
                # hook was already running
                else:
                    del(hook["__rundir"])
                rc = self.hooks[hook["name"]].start(link, hook.get('args', {}), hook_run_dir, do_apply)

                if rc == RC_OK:
                    logger.log_ok('hooks', '= {}'.format(hook["name"]))
                elif rc == RC_STARTED:
                    logger.log_add('hooks', '+ {}'.format(hook["name"]))
                elif rc == RC_CHANGED:
                    logger.log_change('hooks', '~ {}'.format(hook["name"]))
                else:
                    logger.log_err('hooks', '! {}'.format(hook["name"]))

                run_state.append({
                    "hook": hook,
                    "rundir": hook_run_dir,
                })
        finally:
            dump_yaml_file(state_fn, run_state)
