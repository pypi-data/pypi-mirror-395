import React, {Component} from "react";
import PropTypes from "prop-types";
import {fetch as fetchPolyfill} from 'whatwg-fetch'
import key from "weak-key";
import queryString from "query-string"
import {Editor} from 'primereact/editor';
import AbortController from 'abort-controller';

import classNames from 'classnames';
import {ScrollPanel} from 'primereact/scrollpanel';
import 'rc-collapse/assets/index.css';
import './Conversations.css';
import {mapReverse, hashCode} from "../LinoUtils";
import { quillMention } from '../quillmodules';


export class LinoChatter extends Component {

    editor = React.createRef();

    static propTypes = {
        sendChat: PropTypes.func,
        sendSeenAction: PropTypes.func,
        group_id: PropTypes.number,
        openedconversation: PropTypes.string
    };
    static defaultProps = {
        // open: false,
    };

    constructor(props) {
        super(props);
        this.state = {
            new_message: '',
            chats: [],
            conservation_name: "",
        };

        this.controller = new AbortController();

        this.reload = this.reload.bind(this);
        this.componentDidMount = this.componentDidMount.bind(this);
        this.componentDidUpdate = this.componentDidUpdate.bind(this);

        this.handleChange = this.handleChange.bind(this);
        this.keyPress = this.keyPress.bind(this);
        this.handleFocus = this.handleFocus.bind(this);
        this.consume_server_response = this.consume_server_response.bind(this);
        this.consume_WS_message = this.consume_WS_message.bind(this);

        this.onSubmit = this.onSubmit.bind(this);
        this.header = (<span></span>);
    }

    reload() {

        // todo pageing

        this.setState({
            loading: true,
        });
        let query = {
            fmt: "json",
            rp: key(this),
            // mt: this.props.actorData.content_type, // Should be the master actor's PK, so should be a prop / url param
            an: "loadGroupChat",
            // limit: 10,
            // count: 10,
        };
        window.App.add_su(query);
        fetchPolyfill(`api/chat/ChatGroup/` + `${this.props.group_id || "-99998"}` + `?${queryString.stringify(query)}`).then(
            window.App.handleAjaxResponse
        ).then(this.consume_server_response
        ).catch(window.App.handleAjaxException);
    }

    consume_server_response(data) {
        let chats_data = data.rows[0];
        console.log('chats_data', chats_data)
        // this.input.current.focus();
        this.setState({
            chats: chats_data.messages,
            conservation_name: chats_data.name,
            // NotSeenChats: chats_data.messages.filter(msg => msg[3] !== undefined).map(msg => msg[3]),
            scroll: new Date() + ""
        })
        console.log('state', this.state)
    }

    componentDidMount() {
        this.reload();
    }

    componentDidUpdate(p, s) {
        if (this.state.scroll !== s.scroll) {
            setTimeout(() => (this.scrollToBottom()), 100)
        }

    }

    consume_WS_message(chat) {
        console.log("got WS chat message", this, chat);
        this.setState(old => {
            let {chats} = old;
            let update_index = chats.findIndex(c => c[7] === chat[7]); // find matching HASH
            if (update_index >= 0) {
                chats = chats.slice();
                chats[update_index] = chat
            } else {
                chats = [chat].concat(old.chats)
            }
            return {
                chats: chats,
                scroll: new Date() + ""
            }
        })

    }

    scrollToBottom = () => {
        this.chatBottom && this.chatBottom.scrollIntoView({behavior: 'smooth', block: 'nearest', inline: 'start'})
        // this.input.current.scrollIntoView({behavior: 'smooth'})
    }

    handleChange(e) {
        let value = e.htmlValue || "";
        this.setState({new_message: value})
    }

    handleFocus(e) {
        //let chatids = this.state.chats.map(msg => msg[4])
        // console.log('handleFocus',this.state.NotSeenChats)
        this.props.sendSeenAction(this.props.group_id/*, this.state.chats.filter(chat => chat[3] === null)*/);
        // this.state.NotSeenChats = [];
    }

    createChatArray(chatHTML) {
        // self.user.username,
        // ar.parse_memo(self.chat.body),
        // json.loads(json.dumps(self.created, cls=DjangoJSONEncoder)),
        // json.loads(json.dumps(self.seen, cls=DjangoJSONEncoder)),
        // self.chat.pk,
        // self.chat.user.id,
        // self.chat.group.id
        // hash
        let date = new Date() + "";
        return [window.App.state.user_settings.username,
            chatHTML,
            date,
            undefined,
            undefined,
            window.App.state.user_settings.user_id,
            this.props.group_id,
            hashCode(chatHTML + date) + ""]
    }

    onSubmit(messageHTML) {
        let chatMSG = this.createChatArray(messageHTML);
        this.props.sendChat({'body': messageHTML, 'hash': chatMSG[7], 'group_id': this.props.group_id});
        this.setState((old) => (
                {chats: [chatMSG].concat(old.chats)}
            )
        );
    }

    keyPress(e) {
        if (e.keyCode === 13 && e.target.innerText) {
            this.onSubmit(e.target.innerText);
            e.target.innerText = "";
        }
    }

    focus() {
        this.editor.quill.focus();
    }


    render_chat_message(userName, userID, currentUserID, sentDateTime, chatHTML, chatPK, hash) {
        let selfChat = currentUserID === userID;
        return <div key={hash}>
            <div style={{
                display: "flex",
                direction: (selfChat ? "rtl" : "ltr")
            }}>
                <span className={"user"}>{userName}</span>
            </div>
            <div className={classNames("message-wrapper", {"not-sent": chatPK === undefined})}
                 style={{
                     display: "flex",
                     flexDirection: selfChat ? "row-reverse" : "row",
                     [selfChat ? "marginLeft" : "marginRright"]: "1em",
                 }}>
                <div title={sentDateTime}
                     style={{background: selfChat ? "#07bdf4" : "#06b4f1"}}
                     className={"message"}
                     dangerouslySetInnerHTML={{__html: chatHTML || "\u00a0"}}/>
            </div>
        </div>
    }

    render() {
        let actorID = "tickets/Tickets";
        return <div
            className="chatwindow"
            onMouseEnter={this.handleFocus}>
            <ScrollPanel className={"chatwindow-chats"} style={{height: "302px"}}>
                {this.state.chats && mapReverse(this.state.chats, (chat) => {

                    // (cp.user.username, ar.parse_memo(cp.chat.body), cp.created, cp.seen, cp.chat.pk, cp.chat.user.id))
                    let userName = chat[0],
                        userID = chat[5],
                        currentUserID = window.App.state.user_settings.user_id,
                        chatHTML = chat[1],
                        sentDateTime = chat[2],
                        seenDateTime = chat[3],
                        chatPK = chat[4],
                        hash = chat[7];

                    return this.render_chat_message(userName, userID, currentUserID, sentDateTime, chatHTML, chatPK, hash)
                })}
                <div ref={(el) => this.chatBottom = el} style={{height: "1ch"}}/>
            </ScrollPanel>
            <div
                onKeyDown={(e) => {
                    if ([13, 9, 33, 34, 35, 36, 46].includes(e.keyCode)) {
                        e.stopPropagation();
                    }
                    if (e.keyCode === 13 && e.shiftKey) {
                        this.keyPress(e);
                        e.preventDefault();
                        e.stopPropagation();
                    }
                }}>
                <Editor
                    modules={{
                        mention: quillMention(this.controller.signal),
                    }}
                    style={{height: '100%', width: "281.7px"}}
                    headerTemplate={this.header}
                    placeholder={"Write to group..."}
                    ref={e => this.editor = e}
                    onTextChange={this.handleChange}/>
            </div>
        </div>
    }
};
