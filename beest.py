from textual import on
from textual.app import App, ComposeResult, RenderResult
from textual.widgets import Button, RichLog
from textual.app import App, ComposeResult
from textual.widget import Widget
from textual.widgets import (
    Header,
    Footer,
    Tree,
    Static,
    Button,
    Log,
    Label,
    ContentSwitcher,
    Markdown,
    LoadingIndicator, TabbedContent, TabPane,
    RadioButton, RadioSet,
    Rule, Switch, Select, Input, Tabs
)
from textual.containers import Container, VerticalScroll, Horizontal, Vertical, Center
from textual.screen import Screen
from rich.console import Console
from rich.text import Text
import asyncio
from datetime import datetime
import subprocess
import os
import glob


def banner():
    return '''




██████╗ ███████╗███████╗███████╗████████╗ 0.1.0
██╔══██╗██╔════╝██╔════╝██╔════╝╚══██╔══╝ 
██████╔╝█████╗  █████╗  ███████╗   ██║    
██╔══██╗██╔══╝  ██╔══╝  ╚════██║   ██║    
██████╔╝███████╗███████╗███████║   ██║    
╚═════╝ ╚══════╝╚══════╝╚══════╝   ╚═╝    

A swiss army knife for the Swarm ecosystem
'''


class BusyPopup(Screen):
    def compose(self) -> ComposeResult:
        yield LoadingIndicator(id="popup")


class Page(VerticalScroll):
    BEEST_DIR = os.path.expanduser("~/.beest")
    def set_busy(self, busy: bool):
        if busy:
            self.app.push_screen(BusyPopup())
        else:
            self.app.pop_screen()

    def logr(self, id=''):
        if(id != ''):
            return self.query_one("#"+id, Logr)
        return self.query_one(Logr)

    def root(self):
        root = next(
            (item for item in self.ancestors if isinstance(item, Beest)), None)
        return root


class Config:
    BEGIN_PORT = 6699


class State:
    BEES = 0


class Logr(RichLog):
    markup = True
    highlight = True

    def out(self, msg, *args, **kwargs):
        super(self.__class__, self).write(f"{msg}", *args, **kwargs)

    def log(self, msg, *args, **kwargs):
        super(self.__class__, self).write(
            f"[cyan][INFO][/cyan] {msg}", *args, **kwargs)

    def err(self, msg, *args, **kwargs):
        super(self.__class__, self).write(
            f"[red][ERROR] {msg}[/red] ", *args, **kwargs)


class Util:
    @staticmethod
    def now():
        return datetime.now().strftime("%Y-%m-%d %H:%M:%S")

    @staticmethod
    async def run_script(cmd, script_file, args, page: Page, logr: Logr):
        exec_cmd = [cmd, f"{os.getcwd()}/scripts/{script_file}", *args]
        logr.clear()
        print(
            f"EXECUTING: [code]{ ' '.join(str(item) for item in exec_cmd) }[/code]")
        # exit(0)
        process = await asyncio.create_subprocess_exec(
            *exec_cmd,
            stdout=asyncio.subprocess.PIPE,
            stderr=asyncio.subprocess.PIPE
        )
        page.set_busy(True)
        print(f"subprocess: {process}")
        while True:
            line = await process.stdout.readline()
            if line:
                logr.out(line.decode("utf-8").rstrip())
            else:
                break
        _, stderr = await process.communicate()
        if stderr:
            logr.err(stderr.decode("utf-8").rstrip())
        await process.wait()
        page.set_busy(False)

    @staticmethod
    def dasherize(string):
        lowercase_string = str(string).lower()
        replaced_string = lowercase_string.replace(" ", "-")
        return replaced_string


class InstallPage(Page):
    async def show_outdated(self):
        await Util.run_script('bash', 'show_outdated.sh', [], self, self.logr())

    def on_button_pressed(self, event: Button.Pressed) -> None:
        self.logr().clear()
        event.prevent_default()
        self.run_worker(self.show_outdated(), exclusive=True)

    def compose(self) -> ComposeResult:
        with Vertical():
            yield Markdown("# BEEST / Install")
            with Center():
                yield Button("Show Installed Packages", id="show-installed")
            yield Logr(markup=True)


class InstallBeePage(Page):
    async def install_bee(self):
        await Util.run_script('bash', 'install_bee.sh', [], self, self.logr())
        self.logr().write("\n"+self.installed_bee_versions())

    def on_button_pressed(self, event: Button.Pressed) -> None:
        self.logr().clear()
        event.prevent_default()
        self.run_worker(self.install_bee(), exclusive=True)

    def installed_bee_versions(self):
        try:
            files = os.listdir(Beest.BIN_PATH)
            files.remove('bee')
        except Exception:
            files = ['None']
        return '[cyan]Installed Bee versions:[/cyan][green]\n'+'\n'.join([" - " + item[4:] for item in files])+'\n[/green]'

    def compose(self) -> ComposeResult:
        try:
            files = os.listdir(Beest.BIN_PATH)
            files.remove('bee')
        except Exception:
            files = ['None']

        with Vertical():
            yield Markdown("# BEEST / Install / Bee")
            with Center():
                yield Button("Install Latest Bee + Tools", id="install-bee")
            yield Logr(markup=True).write(self.installed_bee_versions())


class InstallEtherproxyPage(Page):
    async def install_etherproxy(self):
        await Util.run_script('bash', 'install_etherproxy.sh', [], self, self.logr())
        # self.logr().write("\n"+self.installed_bee_versions())

    def on_button_pressed(self, event: Button.Pressed) -> None:
        self.logr().clear()
        event.prevent_default()
        self.run_worker(self.install_etherproxy(), exclusive=True)

    def compose(self) -> ComposeResult:
        with Vertical():
            yield Markdown("# BEEST / Install / Etherproxy")
            with Center():
                yield Button("Install Etherproxy", id="install-etherproxy")
            yield Logr(markup=True)


class InstallBeeFactoryPage(Page):
    async def install_bee_factory(self):
        await Util.run_script('bash', 'install_bee_factory.sh', [], self, self.logr())

    def on_button_pressed(self, event: Button.Pressed) -> None:
        self.logr().clear()
        event.prevent_default()
        self.run_worker(self.install_bee_factory(), exclusive=True)

    def compose(self) -> ComposeResult:
        with Vertical():
            yield Markdown("# BEEST / Install / Bee Factory")
            with Center():
                yield Button("Install Bee Factory", id="install-bee-factory")
            yield Logr(markup=True)


class InstallFdpPlayPage(Page):
    async def install_fdp_play(self):
        await Util.run_script('bash', 'install_fdp_play.sh', [], self, self.logr())

    def on_button_pressed(self, event: Button.Pressed) -> None:
        self.logr().clear()
        event.prevent_default()
        self.run_worker(self.install_fdp_play(), exclusive=True)

    def compose(self) -> ComposeResult:
        with Vertical():
            yield Markdown("# BEEST / Install / FDP Play")
            with Center():
                yield Button("Install FDP Play", id="install-fdp-play")
            yield Logr(markup=True)


class BeestPage(Page):
    def compose(self) -> ComposeResult:
        with Horizontal(classes="banner"):
            with Center():
                yield Label(banner())


class RunPage(Page):
    pass


class MonitorPage(Page):
    pass


class SettingsPage(Page):
    pass


class BeeMonitorPage(Page):
    active_bee = ""

    def compose(self) -> ComposeResult:
        with Vertical():
            yield Markdown(f"# BEEST / Monitor / Bee")
            with TabbedContent():
                with TabPane("Overview",id="overview-tab"):
                    yield Button("Show Bee Info", id="overview")
                with TabPane("Logs (HEAD)", id="out-head"):
                    yield Markdown("")
                    yield Button("Show Logs (BEGIN)", id="out-begin")
                with TabPane("Logs (TAIL)", id="out-tail"):
                    yield Markdown("")
                    yield Button("Show Logs (END)", id="out-end")
                with TabPane("Errors (HEAD)", id="err-head"):
                    yield Markdown("")
                    yield Button("Show Error Logs (BEGIN)", id="err-begin")
                with TabPane("Errors (TAIL)", id="err-tail"):
                    yield Markdown("")
                    yield Button("Show Error Logs (END)", id="err-end")
            yield Logr(markup=True)
    
    @on(TabbedContent.TabActivated)
    def tab_changed(self, event: TabbedContent.TabActivated):
        # self.logr().write(f"Switched to {event.tab.label}")
        pass

    def on_button_pressed(self, event: Button.Pressed) -> None:
        self.logr().clear().write(f"{self.active_bee},{event.button.id}")
        event.prevent_default()
        match event.button.id:
            case 'out-begin':
                self.run_worker(self.show_log('head','out'), exclusive=True)
            case 'out-end':
                self.run_worker(self.show_log('tail','out'), exclusive=True)
            case 'err-begin':
                self.run_worker(self.show_log('head','error'), exclusive=True)
            case 'err-end':
                self.run_worker(self.show_log('tail','error'), exclusive=True)
            case 'overview':
                self.run_worker(self.show_overview(), exclusive=True)
    
    async def show_overview(self):
        await Util.run_script('python', 'bee_overview.py', [str(self.active_bee)], self, self.logr())
    async def show_log(self, head_or_tail, error_or_out):
        await Util.run_script('bash', 'get_logs.sh', [f"{head_or_tail}", f"{self.active_bee.replace('_', '-')}", f"{error_or_out}"], self, self.logr())
        # self.logr().write("hello")


verbosityOptions = [("0: silent", 0), ("1: error", 1), ("2: warn", 2),
                    ("3: info", 3), ("4: debug", 4), ("5: trace", 5)]


class RunBeePage(Page):
    def on_select_changed(self, event: Select.Changed):
        # self.logr().write(f"{event.select.value}")
        pass

    async def run_bee_ultralight(self):
        await Util.run_script('python3', 'run_bee.py', [
            '--mode', 'ultralight',
            '--verbosity', str(self.query_one('#verbosity-ul', Select).value),
            '--nbhood', self.query_one('#nbhood', Input).value
        ], self, self.logr())
        self.root().updateTree()
        # self.logr().write(root.tree)

    async def run_bee_light(self):
        await Util.run_script('python3', 'run_bee.py', [
            '--mode', 'light',
            '--rpc', self.query_one('#gnosis-rpc', Input).value,
            '--verbosity', str(self.query_one('#verbosity-l', Select).value)
        ], self, self.logr())

    async def run_bee_full(self):
        await Util.run_script('python3', 'run_bee.py', [
            '--mode', 'full',
            '--rpc', self.query_one('#gnosis-rpc', Input).value,
            '--verbosity', str(self.query_one('#verbosity-l', Select).value)
        ], self, self.logr())
    
    def bee_count(self):
        return len(glob.glob(f"{self.BEEST_DIR}/bees/scripts/*.sh"))
    
    async def delete_bees(self):
        await Util.run_script('python3', 'delete_bees.py', [], self, self.logr())
        self.root().updateTree()

    async def show_bees(self):
        await Util.run_script('python3', 'show_bees.py', [], self, self.logr())

    async def stop_bees(self):
        await Util.run_script('python3', 'stop_bees.py', [], self, self.logr())
    
    async def start_bees(self):
        
        await Util.run_script('python3', 'start_bees.py', [], self, self.logr())

    @on(TabbedContent.TabActivated)
    def tab_changed(self, event: TabbedContent.TabActivated):
        # self.logr().write(f"Switched to {event.tab.label}")
        pass

    def compose(self) -> ComposeResult:
        yield Markdown("# Run Bee")
        with TabbedContent():
            with TabPane("RUN A BEE NODE", id="run-bee"):
                yield Markdown("")
                # with TabbedContent():
                #     with TabPane("ULTRALIGHT NODE", id="bee-ultralight"):
                yield Markdown("")
                with Horizontal():
                    yield Label("Neighbourhood:")
                    yield Input(placeholder="Target Neigbourhood", id="nbhood", value="")
                with Horizontal():
                    yield Label("Verbosity:")
                    yield Select(verbosityOptions, id="verbosity-ul", value=5)
                with Horizontal(classes="submit"):
                    yield Button("Run a mainnet node", id="ultralightnode")
                    yield Button("Run a testnet node", id="ultralightnode-test")
                    # with TabPane("LIGHT NODE", id="bee-light"):
                    #     yield Markdown("")
                    #     with Horizontal():
                    #         yield Label("Gnosis RPC URL:")
                    #         yield Input(placeholder="Gnosis RPC Endpoint [or] Etherproxy URL", id="gnosis-rpc-l", value="")
                    #     with Horizontal():
                    #         yield Label("Verbosity:")
                    #         yield Select(verbosityOptions, id="verbosity-l", value=5)
                    #     with Horizontal(classes="submit"):
                    #         yield Button("Run a light node", id="lightnode")
                    # with TabPane("FULL NODE", id="bee-full"):
                    #     yield Markdown("")
                    #     with Horizontal():
                    #         yield Label("Gnosis RPC URL:")
                    #         yield Input(placeholder="Gnosis RPC Endpoint [or] Etherproxy URL", id="gnosis-rpc", value="")
                    #     with Horizontal():
                    #         yield Label("Verbosity:")
                    #         yield Select(verbosityOptions, id="verbosity-f", value=5)
                    #     with Horizontal(classes="submit"):
                    #         yield Button("Run a Fullnode", id="fullnode")
                    # with TabPane("DEV MODE", id="bee-dev"):
                    #     yield Markdown("")
                    #     yield Button("Run Bee in developer mode", id="devmode")
            with TabPane("SHOW BEES", id="bee-show"):
                yield Markdown("")
                yield Button("Show all bees", id="show_bees")
            with TabPane("START BEES", id="bee-start"):
                yield Markdown("")
                yield Button("Start all bees", id="start_bees")
            with TabPane("STOP BEES", id="bee-stop"):
                yield Markdown("")
                yield Button("Stop all bees", id="stop_bees")
            with TabPane("DELETE BEES", id="bee-delete"):
                yield Markdown("")
                with Horizontal():
                    yield Button("Delete all bees", id="delete_bees")
        yield Logr(markup=True)

    def on_button_pressed(self, event: Button.Pressed) -> None:
        cmd = ""
        match event.button.id:
            case 'ultralightnode':
                cmd = f"bee start --full-node=false --swap-enable=false --debug-api-enable=true --verbosity={self.query_one('#verbosity-ul',Select).value}"
                event.prevent_default()
                self.logr().write( f" {self.query_one('#nbhood',Input).value} " )
                self.run_worker(self.run_bee_ultralight(), exclusive=True)
            case 'lightnode':
                rpc_input = self.query_one('#gnosis-rpc-l', Input)
                if(rpc_input.value == ""):
                    self.logr().clear().err("Gnosis RPC URL cannot be empty!")
                    rpc_input.focus()
                    return
                cmd = f"bee start --full-node=false --swap-enable=false --debug-api-enable=true --verbosity={self.query_one('#verbosity-l',Select).value}"
                event.prevent_default()
                self.run_worker(self.run_bee_light(), exclusive=True)
            case 'fullnode':
                rpc_input = self.query_one('#gnosis-rpc', Input)
                if(rpc_input.value == ""):
                    self.logr().clear().err("Gnosis RPC URL cannot be empty!")
                    rpc_input.focus()
                    return
                cmd = f"bee start --full-node=false --swap-enable=false --debug-api-enable=true --verbosity={self.query_one('#verbosity-f',Select).value}"
                event.prevent_default()
                self.run_worker(self.run_bee_full(), exclusive=True)
            case 'delete_bees':
                event.prevent_default()
                if(self.bee_count() > 0):
                    self.run_worker(self.delete_bees(), exclusive=True)
                else:
                    self.logr().write('No bees to delete!')
            case 'show_bees':
                event.prevent_default()
                if(self.bee_count() > 0):
                    self.run_worker(self.show_bees(), exclusive=True)
                else:
                    self.logr().write('No bees to show!')
            case 'stop_bees':
                event.prevent_default()
                if(self.bee_count() > 0):
                    self.run_worker(self.stop_bees(), exclusive=True)
                else:
                    self.logr().write('No bees to stop!')
            case 'start_bees':
                event.prevent_default()
                if(self.bee_count() > 0):
                    self.run_worker(self.start_bees(), exclusive=True)
                else:
                    self.logr().write('No bees to start!')


class Beest(App[str]):

    default_page = "page-beest"
    CSS_PATH = "./style.tcss"
    BINDINGS = [
        ("d", "toggle_dark", "Toggle dark mode"),
        ("q", "quit", "Quit"),
    ]
    APP_PATH = os.path.expanduser("~/.beest")
    BIN_PATH = APP_PATH + "/bin/bee"
    tree: Tree[dict] = Tree("BEEST", id="sidebar")

    def updateTree(self):
        bee_scripts = glob.glob(f"{self.APP_PATH}/bees/scripts/*.sh")
        bee_scripts = [os.path.splitext(os.path.basename(path))[
            0] for path in bee_scripts]
        bee_scripts.sort()
        bees = self.tree.get_node_by_id(8)
        bees.remove_children()
        for i, bee_script in enumerate(bee_scripts):
            bees.add_leaf(f"{i+1}: {bee_script}")

    def Sidebar(self):
        install = self.tree.root.add("INSTALL", expand=True)
        install.add_leaf("Bee")
        install.add_leaf("Etherproxy")
        install.add_leaf("Bee Factory")
        install.add_leaf("FDP Play")

        install = self.tree.root.add("RUN", expand=True)
        install.add_leaf("Bee")
        # install.add_leaf("Bee Factory")
        # install.add_leaf("FDP Play")

        install = self.tree.root.add("MONITOR", expand=True)
        # install.add_leaf("Bee001")
        # install.add_leaf("Bee002")
        # install.add_leaf("Bee003")
        # install.add_leaf("Bee004")

        install = self.tree.root.add("SETTINGS", expand=True)
        # install.add_leaf("Bee")
        # install.add_leaf("Etherproxy")

        self.tree.root.expand_all()
        return self.tree

    def compose(self) -> ComposeResult:
        with Vertical():
            yield Header("BEEST")
            with Horizontal():
                yield self.Sidebar()
                self.updateTree()
                with ContentSwitcher(id="switch", initial=self.default_page):
                    yield BeestPage(id="page-beest")
                    yield InstallPage(id="page-beest-install")
                    yield InstallBeePage(id="page-install-bee")
                    yield InstallEtherproxyPage(id="page-install-etherproxy")
                    yield InstallBeeFactoryPage(id="page-install-bee-factory")
                    yield InstallFdpPlayPage(id="page-install-fdp-play")
                    yield RunPage(id="page-beest-run")
                    yield RunBeePage(id="page-run-bee")
                    yield MonitorPage(id="page-beest-monitor")
                    yield SettingsPage(id="page-beest-settings")
                    yield BeeMonitorPage(id="page-bee-monitor")
            # yield Logr(id="mainlogr")
            yield Footer()

    def on_button_pressed(self, event: Button.Pressed) -> None:
        pass

    def on_tree_node_selected(self, event: Tree.NodeSelected) -> None:
        # self.query_one("#mainlogr",Logr).write(f"{event.node.id} {event.node.label}")
        self.query_one(Tree).root.expand_all()
        if event.node.id == 0:
            nodeid = "page-beest"
        else:
            nodeid = f"page-{Util.dasherize(event.node.parent.label)}-{Util.dasherize(event.node.label)}"
        try:
            self.query_one("#switch", ContentSwitcher).current = nodeid
        except Exception as err:
            # self.query_one("#mainlogr", Logr).write(event.node.label)
            beePage = self.query_one("#page-bee-monitor")
            beePage.active_bee = str(event.node.label.split(': ').pop())
            beePage.logr().clear()
            beePage.query_one('#overview',Button).label = f"Show Info: {beePage.active_bee.upper()} "
            self.query_one(
                "#switch", ContentSwitcher).current = "page-bee-monitor"

    def on_mount(self):
        pass


if __name__ == "__main__":
    app = Beest()
    app.run()
