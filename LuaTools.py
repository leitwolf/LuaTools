import sublime
import sublime_plugin
import functools
import os
import datetime

def isST3():
    return sublime.version()[0] == '3'

if isST3():
    from .luatoolslib import helper
else:
    from luatoolslib import helper
    # reload(helper)


PACKAGE_NAME = "LuaTools"
LIB_PATH="luatoolslib"

# init plugin
def init():
    settings=loadSettings()
    settings.clear_on_change(PACKAGE_NAME)
    settings.add_on_change(PACKAGE_NAME, settingsChanged)


def settingsChanged():
    settings=loadSettings()
    # system api
    s=settings.get("system","")
    arr=["5.1","5.2"]
    if s not in arr:
        sublime.error_message("LuaTools: Settings->system invalid!")
    else:
        dir=os.path.join(sublime.packages_path(),PACKAGE_NAME,LIB_PATH,"system-api")
        for str in arr:
            oldname=""
            newname=""
            if s==str:
                oldname="lua%s.sublime-completions-nouse"%(str)
                newname="lua%s.sublime-completions"%(str)                
            else:
                oldname="lua%s.sublime-completions"%(str)     
                newname="lua%s.sublime-completions-nouse"%(str)
            old=os.path.join(dir,oldname)
            new=os.path.join(dir,newname)
            if os.path.exists(old):
                os.rename(old,new)               
                
    

class LuaToolsNewFileCommand(sublime_plugin.WindowCommand):

    def run(self, dirs):
        self.window.run_command("hide_panel")
        title = "untitle"
        on_done = functools.partial(self.on_done, dirs[0])
        v = self.window.show_input_panel(
            "File Name:", title + ".lua", on_done, None, None)
        v.sel().clear()
        v.sel().add(sublime.Region(0, len(title)))

    def on_done(self, path, name):
        filePath = os.path.join(path, name)
        if os.path.exists(filePath):
            sublime.error_message("Unable to create file, file exists.")
        else:
            # load template file
            tmplPath = os.path.join(
                sublime.packages_path(), PACKAGE_NAME, LIB_PATH, "lua.tmpl")
            code = helper.readFile(tmplPath)
            # add attribute
            settings = loadSettings()
            format = settings.get("date_format", "%Y-%m-%d %H:%M:%S")
            date = datetime.datetime.now().strftime(format)
            code = code.replace("${date}", date)
            attr = settings.get("template_attr", {})
            for key in attr:
                code = code.replace("${%s}" % (key), attr.get(key, ""))
            # save
            helper.writeFile(filePath, code)
            v=sublime.active_window().open_file(filePath)
            # cursor
            v.run_command("insert_snippet",{"contents":code})
            sublime.status_message("Lua file create success!")

    def is_enabled(self, dirs):
        return len(dirs) == 1

def loadSettings():
    return sublime.load_settings(PACKAGE_NAME + ".sublime-settings")

# st3
def plugin_loaded():
    sublime.set_timeout(init, 200)

# st2
if not isST3():
    init()
