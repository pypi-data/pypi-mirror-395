export const name = "AppMenu";

import './AppMenu.css';

import React from "react";
import PropTypes from 'prop-types';
import { RegisterImportPool, getExReady, Component } from "./Base";

let ex; const exModulePromises = ex = {
    classNames: import(/* webpackChunkName: "classNames_Appmenu" */"classnames"),
}
RegisterImportPool(ex);

class AppSubmenu extends Component {
    static requiredModules = ["classNames"];
    static iPool = ex;

    static defaultProps = {
        className: null,
        items: null,
        onMenuItemClick: null,
        root: false
    }

    static propTypes = {
        className: PropTypes.string,
        items: PropTypes.array,
        onMenuItemClick: PropTypes.func,
        root: PropTypes.bool
    }

    constructor(props) {
        super(props);
        this.state = {
            ...this.state,
            activeIndex: null};
    }

    onMenuItemClick(event, item, index) {
        //avoid processing disabled items
        if(item.disabled) {
            event.preventDefault();
            return true;
        }

        //execute command
        if(item.command) {
            if (event.ctrlKey) {
                let newWindow = window.open(document.URL), count = 0;
                const waitForMountAndRun = () => {
                    if (newWindow.hasOwnProperty('App') && !newWindow.App.state.site_loading) {
                        let it = null;
                        const iterItems = (items) => {
                            items.every((i) => {
                                if (it !== null) {
                                    return false;
                                }
                                if (i.hasOwnProperty('items')) {
                                    iterItems(i.items)
                                } else if (i.id === item.id) {
                                    it = i;
                                    return false;
                                }
                                return true;
                            })
                        }
                        iterItems(newWindow.App.state.menu_data);
                        newWindow.command = it.command;
                        newWindow.command({originalEvent: event, item: it});
                    } else {
                        if (count > 20) return;
                        count += 1;
                        setTimeout(() => waitForMountAndRun(), 100);
                    }
                }
                waitForMountAndRun()
            } else item.command({originalEvent: event, item: item});
        }

        //prevent hash change
        if(item.items || !item.url) {
            event.preventDefault();
        }

        if(index === this.state.activeIndex)
            this.setState({activeIndex: null});
        else
            this.setState({activeIndex: index});

        if(this.props.onMenuItemClick) {
            this.props.onMenuItemClick({
                originalEvent: event,
                item: item
            });
        }
    }

    render() {
        if (!this.state.ready) return null;
        let items = this.props.items && this.props.items.map((item, i) => {
            if (item === "is_a_seperator") {
                return <hr key={i}/>
            }
            let active = this.state.activeIndex === i;
            let styleClass = this.ex.classNames.default(
                item.badgeStyleClass, {'active-menuitem': active});
            styleClass += " l-menuitem"
            if (item.id === this.props.activeElemId) styleClass += " l-linked-menu";
            let badge = item.badge
                && <span className="menuitem-badge">{item.badge}</span>;
            let submenuIcon = item.items
                && <i className="pi pi-fw pi-angle-down menuitem-toggle-icon"></i>;

            return (
                <li className={styleClass} key={i} id={item.id}>
                    {item.items && this.props.root===true && <div className='arrow'></div>}
                    <a
                        href={item.url}
                        onClick={(e) => {
                            this.onMenuItemClick(e, item, i);
                        }}
                        target={item.target}>
                        <i className={item.icon}></i>
                        <span>{item.label}</span>
                        {submenuIcon}
                        {badge}
                    </a>
                    <AppSubmenu
                        activeElemId={this.props.activeElemId}
                        items={item.items}
                        onMenuItemClick={this.props.onMenuItemClick}/>
                </li>
            );
        });

        return items ? <ul className={this.props.className}>{items}</ul> : null;
    }
}

export class AppMenu extends React.Component {

    static defaultProps = {
        model: null,
        onMenuItemClick: null
    }

    static propTypes = {
        model: PropTypes.array,
        onMenuItemClick: PropTypes.func
    }
    constructor(props) {
        super(props);
        this.state = {
            navKeys: ["ArrowDown", "ArrowLeft", "ArrowUp",
                "ArrowRight", "Enter", "NumpadEnter"],
            activeNavKeys: false,
        }
        this.data = {
            elemStore: window.App.data.miStore,
            activeElemId: null,
        }
        this.onKeyDown = this.onKeyDown.bind(this);
        this.onMenuTrigger = this.onMenuTrigger.bind(this);
        this.walkDown = this.walkDown.bind(this);
        this.walkUp = this.walkUp.bind(this);
        this.walkRight = this.walkRight.bind(this);
        this.walkLeft = this.walkLeft.bind(this);
    }

    componentDidMount() {
        window.addEventListener('keydown', this.onKeyDown);
    }

    componentWillUnmount() {
        window.removeEventListener('keydown', this.onKeyDown);
    }

    matchId(id) {
        return obj => obj.id === id
    }

    walkDown(activeMenus, main_menu) {
        let menu = main_menu,
            last_item = activeMenus.slice(-1)[0];
        activeMenus.forEach(id => {
            if (id !== last_item) {
                let i = menu.findIndex(this.matchId(id));
                menu = menu[i].items;
            } else {
                let li = document.getElementById(id);
                li.classList.remove('active-menuitem');
                let index = menu.findIndex(this.matchId(id));
                if (index < menu.length - 1) {
                    li.classList.remove('l-selected-menu');
                    li = document.getElementById(menu[index+1].id);
                    li.classList.add('l-selected-menu');
                    if (li.getBoundingClientRect().bottom - window.innerHeight < 0) {
                        li.scrollIntoView({block: 'center', behaviour: 'smooth'});
                    }
                } else {
                    if (activeMenus.length > 1) {
                        document.getElementById(activeMenus.slice(-2)[0])
                            .getElementsByTagName('a')[0].click();
                        li.classList.remove('l-selected-menu');
                        activeMenus = activeMenus.slice(0, -1);
                        this.walkDown(activeMenus, main_menu);
                    }
                }
            }
        });
    }

    walkUp(activeMenus, main_menu) {
        let menu = main_menu;
        activeMenus.forEach(id => {
            if (id !== activeMenus.slice(-1)[0]) {
                let i = menu.findIndex(this.matchId(id));
                menu = menu[i].items;
            } else {
                let li = document.getElementById(id);
                li.classList.remove('active-menuitem');
                let index = menu.findIndex(this.matchId(id));
                if (index !== 0) {
                    li.classList.remove('l-selected-menu');
                    li = document.getElementById(menu[index-1].id);
                    li.classList.add('l-selected-menu');
                    if (li.getBoundingClientRect().top < 80) {
                        li.scrollIntoView({block: 'center', behaviour: 'smooth'});
                    }
                } else {
                    if (activeMenus.length > 1) {
                        document.getElementById(activeMenus.slice(-2)[0])
                            .getElementsByTagName('a')[0].click();
                        li.classList.remove('l-selected-menu');
                        activeMenus = activeMenus.slice(0, -1);
                        this.walkUp(activeMenus, main_menu);
                    }
                }
            }
        });
    }

    walkRight(activeMenus, main_menu) {
        let menu = main_menu;
        let li = Array.from(document.getElementsByClassName('l-selected-menu'));
        if (li.length) {
            li[0].classList.remove('l-selected-menu')
        }
        activeMenus.forEach(id => {
            let i = menu.findIndex(this.matchId(id));
            if (id !== activeMenus.slice(-1)[0]) {
                menu = menu[i].items;
            } else {
                this.data.activeElemId = id;
                let sel, li = document.getElementById(menu[i].id);
                if (menu[i].items) {
                    sel = document.getElementById(menu[i].items[0].id);
                    sel.classList.add('l-selected-menu');
                }
                li.getElementsByTagName('a')[0].click();
                if (!sel) {
                    li.classList.add('l-selected-menu');
                    this.onMenuTrigger();
                }
            }
        });
    }

    walkLeft(activeMenus, main_menu) {
        let menu = main_menu;
        if (activeMenus.length > 1) {
            let li = document.getElementById(activeMenus.slice(-1)[0]);
            li.classList.remove('l-selected-menu');
            li.classList.remove('active-menuitem');
            li = document.getElementById(activeMenus.slice(-2)[0]);
            li.getElementsByTagName('a')[0].click();
            li.classList.add('l-selected-menu');
        }
    }

    onMenuTrigger() {
        if (this.state.activeNavKeys) {
            window.postMessage("ArrowsReleased", "*");
            Array.from(document.getElementsByClassName('l-selected-menu'))
                .forEach(s => s.classList.remove('l-selected-menu'));
            Array.from(document.getElementsByClassName('active-menuitem'))
                .forEach(s => s.classList.remove('active-menuitem'));
        } else {
            if (window.App.state.staticMenuInactive)
                window.App.onToggleMenu();
            window.postMessage("ArrowsTaken", "*");
            let act = Array.from(document.getElementsByClassName(
                'active-menuitem'));
            if (act.length) {
                act.slice(-1)[0].classList.add('l-selected-menu');
            } else {
                document.getElementById(this.data.elemStore[0].id)
                    .classList.add('l-selected-menu')
            }
        }
        this.setState({activeNavKeys: !this.state.activeNavKeys});
    }

    onKeyDown(e) {
        if (document.activeElement.value !== "" && document.activeElement.value !== undefined) return
        if ((e.code === "KeyM" && e.altKey) || this.state.activeNavKeys) {
            if (e.code === "KeyM" && e.altKey) {
                let exit_menu = false;
                if (this.state.activeNavKeys) exit_menu = true;
                this.onMenuTrigger()
                if (exit_menu) return
            }
            if (this.state.navKeys.includes(e.code)) {
                e.preventDefault();
                let activeMenus = [],
                    end_iter = false,
                    main_menu = this.data.elemStore,
                    menu = main_menu;

                Array.from(document.getElementsByClassName(
                    'active-menuitem')).forEach(item => {
                    if (!end_iter) {
                        let i = menu.findIndex(this.matchId(item.id));
                        if (i >= 0) {
                            menu = menu[i].items;
                            activeMenus.push(item.id);
                            if (menu === undefined) end_iter = true;
                        } else item.classList.remove('active-menuitem');
                    } else item.classList.remove('active-menuitem');
                });
                if (!activeMenus.length) {
                    activeMenus.push(main_menu[0].id)
                }
                if (activeMenus.length) {
                    let act = document.getElementById(activeMenus.slice(-1)[0]);
                    let sel = Array.from(act.getElementsByClassName('l-selected-menu'));
                    if (sel.length) {
                        activeMenus.push(sel[0].id);
                    } else if (activeMenus.length > 1) {
                        act = document.getElementById(activeMenus.slice(-2)[0]);
                        sel = Array.from(act.getElementsByClassName('l-selected-menu'));
                        if (sel.length) {
                            activeMenus = activeMenus.slice(0, -1);
                            activeMenus.push(sel[0].id);
                        }
                    } else {
                        sel = Array.from(document.getElementsByClassName('l-selected-menu'));
                        if (sel.length) {
                            activeMenus = activeMenus.slice(0, -1);
                            activeMenus.push(sel[0].id);
                        }
                    }
                }
                if (e.code === "ArrowDown") {
                    this.walkDown(activeMenus, main_menu);
                } else if (e.code === "ArrowUp") {
                    this.walkUp(activeMenus, main_menu);
                } else if (this.state.navKeys.slice(-3).includes(e.code)) {
                    this.walkRight(activeMenus, main_menu);
                } else if (e.code === "ArrowLeft") {
                    this.walkLeft(activeMenus, main_menu);
                }
            }
        }
    }

    render() {
        return <div className="menu">
            <AppSubmenu
                activeElemId={this.data.activeElemId}
                items={this.props.model}
                className="layout-main-menu"
                onMenuItemClick={this.props.onMenuItemClick}
                root={true}/>
        </div>
    }
}
