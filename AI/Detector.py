import os
import sqlite3
import hashlib
from multiprocessing import Process
from queue import Queue
from threading import Thread
from frida_hooker import JsHook, JsHooker
from common import load_config
from DBUtils import DBUtils


class Detector:

    def __init__(self, config_file):
        self.config, self.logger = load_config(config_file)
        self.rules, self.white_list = self._get_rules_and_white_list()

    def _get_rules_and_white_list(self):
        """
        Load detection rules from config file.

        :return: A two-element tuple containing a list of detection rules and a dictionary of white list.
        """
        rules, white_list = [], {}
        for k, v in self.config.items("DetectorRules"):
            if k.startswith("rule"):
                rules.append(v)
            elif k.startswith("whitelist"):
                white_list[v.lower()] = True
        return rules, white_list

    def _hash_str(self, s, alg="md5"):
        """
        Compute the hash value of a string.

        :param s: The string to be hashed.
        :param alg: The hash algorithm to use, default is "md5".
        :return: The hash value of the string.
        """
        if alg not in hashlib.algorithms_available:
            raise Exception("Unsupported hash algorithm: {}".format(alg))
        h = hashlib.new(alg)
        h.update(s.encode())
        return h.hexdigest()

    def _check_action(self, action):
        """
        Check whether the given action is a sensitive action.

        :param action: The action to be checked.
        :return: Return True if the action is sensitive, otherwise False.
        """
        # Remove duplicated actions
        if "inc" in action:
            return False
        # Ignore non-sensitive actions
        if action.lower() in self.white_list:
            return False
        # Check sensitive actions
        for r in self.rules:
            if r.strip() == "":
                continue
            matched = True
            for part in r.lower().split("&"):
                if part.startswith("-"):
                    if part[1:].strip() in action.lower():
                        matched = False
                        break
                else:
                    if part.strip() not in action.lower():
                        matched = False
                        break
            if matched:
                return True
        return False

    def _log_action(self, action, component):
        """
        If the given action is sensitive, record it into SQLite database.

        :param action: The action to be logged.
        :param component: The component to be logged.
        """
        if self._check_action(action):
            uid = self._hash_str(component)
            sql = """INSERT INTO Traces(uid, component, action, tag) VALUES (?, ?, ?, ?)"""
            try:
                self.db.execute((sql, (uid, component, action, self.config.get("DetectorRules", "tag"))))
                self.db.commit()
            except Exception as e:
                self.logger.exception("Failed to insert action into database: {}".format(e))

    def _process_logs(self, queue):
        """
        Read log queue, distinguish sensitive logs and logs that need to be processed, and store the sensitive logs into a database.

        :param queue: The queue to read.
        """
        while True:
            log = queue.get()
            if log is None:
                break
            action, component, data = log.strip().split("\t", 2)
            if self._check_action(action):
                self.logger.warning("{}:\t{}\t{}".format(action, component, data))
            self._log_action(action, component)

    def _get_app_name(self, app_file):
        """
        Get the app name by the app file name.

        :param app_file: The path to the app file.
        :return: The app name.
        """
        return os.path.splitext(os.path.basename(app_file))[0]

    def start_hook(self, app_file):
        """
        Start hooking the specified app.

        :param app_file: The app file to be hooked.
        """
        target_app_name = self._get_app_name(app_file)
        js_hooker = JsHooker(target_app_name, self.logger,
                             js_hook_file=self.config.get("DetectorRules", "js_hook_file"))
        queue = Queue()
        processor_thread = Thread(target=self._process_logs, args=(queue,))
        processor_thread.start()
        try:
            js_hook = JsHook(js_hooker, self.logger, js_hook_script=self.config.get("DetectorRules", "js_hook_script"))
            js_hook.start()
            self.logger.info("hooker start")
            js_hook.evaluate("""Java.perform(function() {
                                    // modify this hook to catch more related content, e.g., shared preference.
                                    const contextWrapper = Java.use('android.content.ContextWrapper');
                                    let app_context_wrapped = false;
                                    contextWrapper.attachBaseContext.implementation = function () {
                                        const base_context = this.attachBaseContext.apply(this, arguments);
                                        if (!app_context_wrapped) {
                                            app_context_wrapped = true;
                                            // search sensitive information in databases
                                            try {
                                                const databaseUtils = Java.use('com.xujiaji.dice.misc.DatabaseUtils');
                                                var appFile = -9223372036854775808;
                                                if (arguments[0] != null) {
                                                    appFile = arguments[0].v10.value;
                                                }

                                                const databases = databaseUtils.getDatabaseNames(base_context, appFile);
                                                var databaseIndex = -1;
                                                var database = null;
                                                for (let i = 0; i< databases.size(); ++i) {
                                                    var dbName = databases.get(i).toString();
                                                    if (dbName.endsWith('db') || dbName.endsWith('db-journal')) {
                                                        databaseIndex = i;
                                                        database = Java.use('com.xujiaji.dice.misc.SQLiteDatabase').openOrCreateDatabase(base_context, appFile, dbName, null);
                                                        break;
                                                    }
                                                }
                                                if (database != null) {
                                                    database.setTraceCallback(
                                                        {
                                                            onOpened: function(db) {console.log('+OPENED: ' + JSON.stringify(arguments)); },
                                                            onExecute: function(db, jsql) {
                                                                console.log('>>>>>>>>>>>> onExecute ' + jsql.$className + "." + jsql.$methodName + ' ' + jsql.$methodReturn + ' <<<<<<<<<<<<');
                                                                if (db && !db.isDbLockedByCurrentThread()) {
                                                                    var component = "";
                                                                    const networkStack = Java.use('android.net.NetworkStack');
                                                                    for (let i in networkStack.SocketRecords){
                                                                        let s = networkStack.SocketRecords[i];
                                                                        if (s.toString().match('LocalSocketAddress \\[.*android.com/dicator.*\\]')) {
                                                                            component = s.toString().match('LocalSocketAddress \\[.*android.com/dicator.*\\]')[0]
                                                                        }
                                                                    }
                                                                    for (let i in jsql.args) {
                                                                        if (jsql.args[i].$className == "java.lang.String") {
                                                                            queue.put(jsql.$className + "." + jsql.$methodName + " " + jsql.args[i].toString() + " " + component)
                                                                        }
                                                                    }
                                                                }
                                                            },
                                                            onCorruption: function(db) {console.log('+CORRUPTION: ' + JSON.stringify(arguments));},
                                                            onClosed: function(db) {console.log('+CLOSED: ' + JSON.stringify(arguments));},
                                                        }
                                                    );
                                                }
                                            } catch (e) {
                                                console.error(e)
                                            }

                                            Java.use('android.webkit.WebView').evaluateJavascript.overload(
                                                'java.lang.String', 'android.webkit.ValueCallback'
                                            ).implementation = function (a, b) {
                                                const content = a.toString();
                                                const data = {
                                                    path: '/evaluate-javascript',
                                                    data: {
                                                        evalContent: content,
                                                    },
                                                    method: 'POST'
                                                };
                                                const component = this.getContext().toString();
                                                queue.put("loadUrl " + component);
                                                b.onReceiveValue.overload('java.lang.Object').call(b, '[HOOK] This evaluateJavascript has been prohibited by frida -- ' + content);
                                            }

                                            Java.use('android.webkit.WebView').loadUrl.overload(
                                                'java.lang.String'
                                            ).implementation = function (a) {
                                                const content = a.toString();
                                                const data = {
                                                    path: '/load-url',
                                                    data: {
                                                        url: content,
                                                    },
                                                    method: 'POST'
                                                };
                                                const component = this.getContext().toString();
                                                queue.put("loadUrl " + component + "\t" + content);
                                                console.warn("HTTP loadUrl!")
                                                callHook(a, component) // 不知道一般什么时候会调用, 在 loadUrl-api里面也加了
                                            };
                                        }
                                        return base_context;
                                    }
                                });""")

            js_hook.join()
            processor_thread.join()
        except Exception as e:
            self.logger.exception(e)
            js_hook.stop()
            processor_thread.join()

    def batch_hook(self, app_folder):
        """
        Hook all apps in the specified folder.

        :param app_folder: The folder that contains the apps to be hooked.
        """
        app_files = [os.path.join(app_folder, f) for f in os.listdir(app_folder)]
        with DBUtils(self.config.get("Database", "db_file"), self.logger) as db:
            self.db = db
            for app_file in app_files:
                self.start_hook(app_file)

    def hook_single_app(self, app_file):
        """
        Hook a single app.

        :param app_file: The app file to be hooked.
        """
        with DBUtils(self.config.get("Database", "db_file"), self.logger) as db:
            self.db = db
            self.start_hook(app_file)


if __name__ == '__main__':
    import argparse

    parser = argparse.ArgumentParser(description="Trace sensitive actions produced by Android apps.")
    parser.add_argument("-c", "--config-file", required=True, help="the configuration file of Detector module")
    parser.add_argument("-f", "--app-folder", help="the folder that contains the apps to be detected")
    parser.add_argument("-a", "--app-file", help="the app file to be detected")

    args = parser.parse_args()

    detector = Detector(args.config_file)
    if args.app_file is not None:
        detector.hook_single_app(args.app_file)
    else:
        detector.batch_hook(args.app_folder)
