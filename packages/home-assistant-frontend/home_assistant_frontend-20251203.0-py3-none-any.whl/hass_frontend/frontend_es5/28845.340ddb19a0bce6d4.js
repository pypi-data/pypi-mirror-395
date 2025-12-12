(self.webpackChunkhome_assistant_frontend=self.webpackChunkhome_assistant_frontend||[]).push([["28845"],{85404:function(t,e,i){"use strict";i(23792),i(44114),i(54743),i(11745),i(16573),i(78100),i(77936),i(18111),i(61701),i(3362),i(42762),i(72107),i(43870),i(48140),i(75044),i(21903),i(91134),i(28845),i(373),i(37467),i(44732),i(79577),i(41549),i(49797),i(49631),i(35623),i(62953);var a=i(40445),n=i(96196),o=i(77845),s=i(94333),r=i(82286),d=i(69150),l=i(88433),c=i(65063),h=i(74209),p=i(36918);i(38962),i(3587),i(75709);let u,g,_,m,v,f,b,x,y,w,k=t=>t;class M extends n.WF{willUpdate(t){this.hasUpdated&&!t.has("pipeline")||(this._conversation=[{who:"hass",text:this.hass.localize("ui.dialogs.voice_command.how_can_i_help")}])}firstUpdated(t){super.firstUpdated(t),this.startListening&&this.pipeline&&this.pipeline.stt_engine&&h.N.isSupported&&this._toggleListening(),setTimeout(()=>this._messageInput.focus(),0)}updated(t){super.updated(t),t.has("_conversation")&&this._scrollMessagesBottom()}disconnectedCallback(){var t;super.disconnectedCallback(),null===(t=this._audioRecorder)||void 0===t||t.close(),this._unloadAudio()}render(){var t,e;const i=!!this.pipeline&&(this.pipeline.prefer_local_intents||!this.hass.states[this.pipeline.conversation_engine]||(0,r.$)(this.hass.states[this.pipeline.conversation_engine],l.ZE.CONTROL)),a=h.N.isSupported,o=(null===(t=this.pipeline)||void 0===t?void 0:t.stt_engine)&&!this.disableSpeech;return(0,n.qy)(u||(u=k` <div class="messages"> ${0} <div class="spacer"></div> ${0} </div> <div class="input" slot="primaryAction"> <ha-textfield id="message-input" @keyup="${0}" @input="${0}" .label="${0}" .iconTrailing="${0}"> <div slot="trailingIcon"> ${0} </div> </ha-textfield> </div> `),i?n.s6:(0,n.qy)(g||(g=k` <ha-alert> ${0} </ha-alert> `),this.hass.localize("ui.dialogs.voice_command.conversation_no_control")),this._conversation.map(t=>(0,n.qy)(_||(_=k` <ha-markdown class="message ${0}" breaks cache .content="${0}"> </ha-markdown> `),(0,s.H)({error:!!t.error,[t.who]:!0}),t.text)),this._handleKeyUp,this._handleInput,this.hass.localize("ui.dialogs.voice_command.input_label"),!0,this._showSendButton||!o?(0,n.qy)(m||(m=k` <ha-icon-button class="listening-icon" .path="${0}" @click="${0}" .disabled="${0}" .label="${0}"> </ha-icon-button> `),"M2,21L23,12L2,3V10L17,12L2,14V21Z",this._handleSendMessage,this._processing,this.hass.localize("ui.dialogs.voice_command.send_text")):(0,n.qy)(v||(v=k` ${0} <div class="listening-icon"> <ha-icon-button .path="${0}" @click="${0}" .disabled="${0}" .label="${0}"> </ha-icon-button> ${0} </div> `),null!==(e=this._audioRecorder)&&void 0!==e&&e.active?(0,n.qy)(f||(f=k` <div class="bouncer"> <div class="double-bounce1"></div> <div class="double-bounce2"></div> </div> `)):n.s6,"M12,2A3,3 0 0,1 15,5V11A3,3 0 0,1 12,14A3,3 0 0,1 9,11V5A3,3 0 0,1 12,2M19,11C19,14.53 16.39,17.44 13,17.93V21H11V17.93C7.61,17.44 5,14.53 5,11H7A5,5 0 0,0 12,16A5,5 0 0,0 17,11H19Z",this._handleListeningButton,this._processing,this.hass.localize("ui.dialogs.voice_command.start_listening"),a?null:(0,n.qy)(b||(b=k` <ha-svg-icon .path="${0}" class="unsupported"></ha-svg-icon> `),"M13,13H11V7H13M13,17H11V15H13M12,2A10,10 0 0,0 2,12A10,10 0 0,0 12,22A10,10 0 0,0 22,12A10,10 0 0,0 12,2Z")))}async _scrollMessagesBottom(){const t=this._lastChatMessage;if(t.hasUpdated||await t.updateComplete,this._lastChatMessageImage&&!this._lastChatMessageImage.naturalHeight)try{await this._lastChatMessageImage.decode()}catch(e){console.warn("Failed to decode image:",e)}t.getBoundingClientRect().y<this.getBoundingClientRect().top+24||t.scrollIntoView({behavior:"smooth",block:"start"})}_handleKeyUp(t){const e=t.target;!this._processing&&"Enter"===t.key&&e.value&&(this._processText(e.value),e.value="",this._showSendButton=!1)}_handleInput(t){const e=t.target.value;e&&!this._showSendButton?this._showSendButton=!0:!e&&this._showSendButton&&(this._showSendButton=!1)}_handleSendMessage(){this._messageInput.value&&(this._processText(this._messageInput.value.trim()),this._messageInput.value="",this._showSendButton=!1)}_handleListeningButton(t){t.stopPropagation(),t.preventDefault(),this._toggleListening()}async _toggleListening(){var t;h.N.isSupported?null!==(t=this._audioRecorder)&&void 0!==t&&t.active?this._stopListening():this._startListening():this._showNotSupportedMessage()}_addMessage(t){this._conversation=[...this._conversation,t]}async _showNotSupportedMessage(){this._addMessage({who:"hass",text:(0,n.qy)(x||(x=k`${0} ${0}`),this.hass.localize("ui.dialogs.voice_command.not_supported_microphone_browser"),this.hass.localize("ui.dialogs.voice_command.not_supported_microphone_documentation",{documentation_link:(0,n.qy)(y||(y=k`<a target="_blank" rel="noopener noreferrer" href="${0}">${0}</a>`),(0,p.o)(this.hass,"/docs/configuration/securing/#remote-access"),this.hass.localize("ui.dialogs.voice_command.not_supported_microphone_documentation_link"))}))})}async _startListening(){this._unloadAudio(),this._processing=!0,this._audioRecorder||(this._audioRecorder=new h.N(t=>{this._audioBuffer?this._audioBuffer.push(t):this._sendAudioChunk(t)})),this._stt_binary_handler_id=void 0,this._audioBuffer=[];const t={who:"user",text:"…"};await this._audioRecorder.start(),this._addMessage(t);const e=this._createAddHassMessageProcessor();try{var i,a;const n=await(0,d.vU)(this.hass,i=>{if("run-start"===i.type)this._stt_binary_handler_id=i.data.runner_data.stt_binary_handler_id,this._audio=new Audio(i.data.tts_output.url),this._audio.play(),this._audio.addEventListener("ended",()=>{this._unloadAudio(),e.continueConversation&&this._startListening()}),this._audio.addEventListener("pause",this._unloadAudio),this._audio.addEventListener("canplaythrough",()=>{var t;return null===(t=this._audio)||void 0===t?void 0:t.play()}),this._audio.addEventListener("error",()=>{this._unloadAudio(),(0,c.showAlertDialog)(this,{title:"Error playing audio."})});else if("stt-start"===i.type&&this._audioBuffer){for(const t of this._audioBuffer)this._sendAudioChunk(t);this._audioBuffer=void 0}else"stt-end"===i.type?(this._stt_binary_handler_id=void 0,this._stopListening(),t.text=i.data.stt_output.text,this.requestUpdate("_conversation"),e.addMessage()):i.type.startsWith("intent-")?e.processEvent(i):"run-end"===i.type?(this._stt_binary_handler_id=void 0,n()):"error"===i.type&&(this._unloadAudio(),this._stt_binary_handler_id=void 0,"…"===t.text?(t.text=i.data.message,t.error=!0):e.setError(i.data.message),this._stopListening(),this.requestUpdate("_conversation"),n())},{start_stage:"stt",end_stage:null!==(i=this.pipeline)&&void 0!==i&&i.tts_engine?"tts":"intent",input:{sample_rate:this._audioRecorder.sampleRate},pipeline:null===(a=this.pipeline)||void 0===a?void 0:a.id,conversation_id:this._conversationId})}catch(n){await(0,c.showAlertDialog)(this,{title:"Error starting pipeline",text:n.message||n}),this._stopListening()}finally{this._processing=!1}}_stopListening(){var t;if(null===(t=this._audioRecorder)||void 0===t||t.stop(),this.requestUpdate("_audioRecorder"),this._stt_binary_handler_id){if(this._audioBuffer)for(const t of this._audioBuffer)this._sendAudioChunk(t);this._sendAudioChunk(new Int16Array),this._stt_binary_handler_id=void 0}this._audioBuffer=void 0}_sendAudioChunk(t){if(this.hass.connection.socket.binaryType="arraybuffer",null==this._stt_binary_handler_id)return;const e=new Uint8Array(1+2*t.length);e[0]=this._stt_binary_handler_id,e.set(new Uint8Array(t.buffer),1),this.hass.connection.socket.send(e)}async _processText(t){this._unloadAudio(),this._processing=!0,this._addMessage({who:"user",text:t});const e=this._createAddHassMessageProcessor();e.addMessage();try{var i;const a=await(0,d.vU)(this.hass,t=>{t.type.startsWith("intent-")&&e.processEvent(t),"intent-end"===t.type&&a(),"error"===t.type&&(e.setError(t.data.message),a())},{start_stage:"intent",input:{text:t},end_stage:"intent",pipeline:null===(i=this.pipeline)||void 0===i?void 0:i.id,conversation_id:this._conversationId})}catch(a){e.setError(this.hass.localize("ui.dialogs.voice_command.error"))}finally{this._processing=!1}}_createAddHassMessageProcessor(){let t="";const e=()=>{"…"!==a.hassMessage.text&&(a.hassMessage.text=a.hassMessage.text.substring(0,a.hassMessage.text.length-1),a.hassMessage={who:"hass",text:"…",error:!1},this._addMessage(a.hassMessage))},i={},a={continueConversation:!1,hassMessage:{who:"hass",text:"…",error:!1},addMessage:()=>{this._addMessage(a.hassMessage)},setError:t=>{e(),a.hassMessage.text=t,a.hassMessage.error=!0,this.requestUpdate("_conversation")},processEvent:n=>{if("intent-progress"===n.type&&n.data.chat_log_delta){const o=n.data.chat_log_delta;if(o.role&&(e(),t=o.role),"assistant"===t){if(o.content&&(a.hassMessage.text=a.hassMessage.text.substring(0,a.hassMessage.text.length-1)+o.content+"…",this.requestUpdate("_conversation")),o.tool_calls)for(const t of o.tool_calls)i[t.id]=t}else"tool_result"===t&&i[o.tool_call_id]&&delete i[o.tool_call_id]}else if("intent-end"===n.type){var o;this._conversationId=n.data.intent_output.conversation_id,a.continueConversation=n.data.intent_output.continue_conversation;const t=null===(o=n.data.intent_output.response.speech)||void 0===o?void 0:o.plain.speech;if(!t)return;"error"===n.data.intent_output.response.response_type?a.setError(t):(a.hassMessage.text=t,this.requestUpdate("_conversation"))}}};return a}constructor(...t){super(...t),this.disableSpeech=!1,this._conversation=[],this._showSendButton=!1,this._processing=!1,this._conversationId=null,this._unloadAudio=()=>{this._audio&&(this._audio.pause(),this._audio.removeAttribute("src"),this._audio=void 0)}}}M.styles=(0,n.AH)(w||(w=k`
    :host {
      flex: 1;
      display: flex;
      flex-direction: column;
    }
    ha-alert {
      margin-bottom: 8px;
    }
    ha-textfield {
      display: block;
    }
    .messages {
      flex: 1;
      display: block;
      box-sizing: border-box;
      overflow-y: auto;
      max-height: 100%;
      display: flex;
      flex-direction: column;
      padding: 0 12px 16px;
    }
    .spacer {
      flex: 1;
    }
    .message {
      font-size: var(--ha-font-size-l);
      clear: both;
      max-width: -webkit-fill-available;
      overflow-wrap: break-word;
      scroll-margin-top: 24px;
      margin: 8px 0;
      padding: 8px;
      border-radius: var(--ha-border-radius-xl);
    }
    @media all and (max-width: 450px), all and (max-height: 500px) {
      .message {
        font-size: var(--ha-font-size-l);
      }
    }
    .message.user {
      margin-left: 24px;
      margin-inline-start: 24px;
      margin-inline-end: initial;
      align-self: flex-end;
      border-bottom-right-radius: 0px;
      --markdown-link-color: var(--text-primary-color);
      background-color: var(--chat-background-color-user, var(--primary-color));
      color: var(--text-primary-color);
      direction: var(--direction);
    }
    .message.hass {
      margin-right: 24px;
      margin-inline-end: 24px;
      margin-inline-start: initial;
      align-self: flex-start;
      border-bottom-left-radius: 0px;
      background-color: var(
        --chat-background-color-hass,
        var(--secondary-background-color)
      );

      color: var(--primary-text-color);
      direction: var(--direction);
    }
    .message.error {
      background-color: var(--error-color);
      color: var(--text-primary-color);
    }
    ha-markdown {
      --markdown-image-border-radius: calc(var(--ha-border-radius-xl) / 2);
      --markdown-table-border-color: var(--divider-color);
      --markdown-code-background-color: var(--primary-background-color);
      --markdown-code-text-color: var(--primary-text-color);
      --markdown-list-indent: 1rem;
      &:not(:has(ha-markdown-element)) {
        min-height: 1lh;
        min-width: 1lh;
        flex-shrink: 0;
      }
    }
    .bouncer {
      width: 48px;
      height: 48px;
      position: absolute;
    }
    .double-bounce1,
    .double-bounce2 {
      width: 48px;
      height: 48px;
      border-radius: var(--ha-border-radius-circle);
      background-color: var(--primary-color);
      opacity: 0.2;
      position: absolute;
      top: 0;
      left: 0;
      -webkit-animation: sk-bounce 2s infinite ease-in-out;
      animation: sk-bounce 2s infinite ease-in-out;
    }
    .double-bounce2 {
      -webkit-animation-delay: -1s;
      animation-delay: -1s;
    }
    @-webkit-keyframes sk-bounce {
      0%,
      100% {
        -webkit-transform: scale(0);
      }
      50% {
        -webkit-transform: scale(1);
      }
    }
    @keyframes sk-bounce {
      0%,
      100% {
        transform: scale(0);
        -webkit-transform: scale(0);
      }
      50% {
        transform: scale(1);
        -webkit-transform: scale(1);
      }
    }

    .listening-icon {
      position: relative;
      color: var(--secondary-text-color);
      margin-right: -24px;
      margin-inline-end: -24px;
      margin-inline-start: initial;
      direction: var(--direction);
      transform: scaleX(var(--scale-direction));
    }

    .listening-icon[active] {
      color: var(--primary-color);
    }

    .unsupported {
      color: var(--error-color);
      position: absolute;
      --mdc-icon-size: 16px;
      right: 5px;
      inset-inline-end: 5px;
      inset-inline-start: initial;
      top: 0px;
    }
  `)),(0,a.__decorate)([(0,o.MZ)({attribute:!1})],M.prototype,"hass",void 0),(0,a.__decorate)([(0,o.MZ)({attribute:!1})],M.prototype,"pipeline",void 0),(0,a.__decorate)([(0,o.MZ)({type:Boolean,attribute:"disable-speech"})],M.prototype,"disableSpeech",void 0),(0,a.__decorate)([(0,o.MZ)({type:Boolean,attribute:!1})],M.prototype,"startListening",void 0),(0,a.__decorate)([(0,o.P)("#message-input")],M.prototype,"_messageInput",void 0),(0,a.__decorate)([(0,o.P)(".message:last-child")],M.prototype,"_lastChatMessage",void 0),(0,a.__decorate)([(0,o.P)(".message:last-child img:last-of-type")],M.prototype,"_lastChatMessageImage",void 0),(0,a.__decorate)([(0,o.wk)()],M.prototype,"_conversation",void 0),(0,a.__decorate)([(0,o.wk)()],M.prototype,"_showSendButton",void 0),(0,a.__decorate)([(0,o.wk)()],M.prototype,"_processing",void 0),M=(0,a.__decorate)([(0,o.EM)("ha-assist-chat")],M)},69709:function(t,e,i){"use strict";var a=i(59787),n=(i(74423),i(23792),i(72712),i(18111),i(22489),i(61701),i(18237),i(3362),i(27495),i(62953),i(40445)),o=i(96196),s=i(77845),r=i(1420),d=i(30015),l=i.n(d),c=i(1087),h=(i(3296),i(27208),i(48408),i(14603),i(47566),i(98721),i(2209));let p;var u=i(996);let g,_=t=>t;const m=t=>(0,o.qy)(g||(g=_`${0}`),t),v=new u.G(1e3),f={reType:(0,a.A)(/((\[!(caution|important|note|tip|warning)\])(?:\s|\\n)?)/i,{input:1,type:3}),typeToHaAlert:{caution:"error",important:"info",note:"info",tip:"success",warning:"warning"}};class b extends o.mN{disconnectedCallback(){if(super.disconnectedCallback(),this.cache){const t=this._computeCacheKey();v.set(t,this.innerHTML)}}createRenderRoot(){return this}update(t){super.update(t),void 0!==this.content&&(this._renderPromise=this._render())}async getUpdateComplete(){return await super.getUpdateComplete(),await this._renderPromise,!0}willUpdate(t){if(!this.innerHTML&&this.cache){const t=this._computeCacheKey();v.has(t)&&((0,o.XX)(m((0,r._)(v.get(t))),this.renderRoot),this._resize())}}_computeCacheKey(){return l()({content:this.content,allowSvg:this.allowSvg,allowDataUrl:this.allowDataUrl,breaks:this.breaks})}async _render(){const t=await(async(t,e,a)=>(p||(p=(0,h.LV)(new Worker(new URL(i.p+i.u("55640"),i.b)))),p.renderMarkdown(t,e,a)))(String(this.content),{breaks:this.breaks,gfm:!0},{allowSvg:this.allowSvg,allowDataUrl:this.allowDataUrl});(0,o.XX)(t.map(t=>m((0,r._)(t))),this.renderRoot),this._resize();const e=document.createTreeWalker(this,NodeFilter.SHOW_ELEMENT,null);for(;e.nextNode();){const t=e.currentNode;if(t instanceof HTMLAnchorElement&&t.host!==document.location.host)t.target="_blank",t.rel="noreferrer noopener";else if(t instanceof HTMLImageElement)this.lazyImages&&(t.loading="lazy"),t.addEventListener("load",this._resize);else if(t instanceof HTMLQuoteElement){var a;const i=(null===(a=t.firstElementChild)||void 0===a||null===(a=a.firstChild)||void 0===a?void 0:a.textContent)&&f.reType.exec(t.firstElementChild.firstChild.textContent);if(i){const{type:a}=i.groups,n=document.createElement("ha-alert");n.alertType=f.typeToHaAlert[a.toLowerCase()],n.append(...Array.from(t.childNodes).map(t=>{const e=Array.from(t.childNodes);if(!this.breaks&&e.length){var a;const t=e[0];t.nodeType===Node.TEXT_NODE&&t.textContent===i.input&&null!==(a=t.textContent)&&void 0!==a&&a.includes("\n")&&(t.textContent=t.textContent.split("\n").slice(1).join("\n"))}return e}).reduce((t,e)=>t.concat(e),[]).filter(t=>t.textContent&&t.textContent!==i.input)),e.parentNode().replaceChild(n,t)}}else t instanceof HTMLElement&&["ha-alert","ha-qr-code","ha-icon","ha-svg-icon"].includes(t.localName)&&i(96175)(`./${t.localName}`)}}constructor(...t){super(...t),this.allowSvg=!1,this.allowDataUrl=!1,this.breaks=!1,this.lazyImages=!1,this.cache=!1,this._renderPromise=Promise.resolve(),this._resize=()=>(0,c.r)(this,"content-resize")}}(0,n.__decorate)([(0,s.MZ)()],b.prototype,"content",void 0),(0,n.__decorate)([(0,s.MZ)({attribute:"allow-svg",type:Boolean})],b.prototype,"allowSvg",void 0),(0,n.__decorate)([(0,s.MZ)({attribute:"allow-data-url",type:Boolean})],b.prototype,"allowDataUrl",void 0),(0,n.__decorate)([(0,s.MZ)({type:Boolean})],b.prototype,"breaks",void 0),(0,n.__decorate)([(0,s.MZ)({type:Boolean,attribute:"lazy-images"})],b.prototype,"lazyImages",void 0),(0,n.__decorate)([(0,s.MZ)({type:Boolean})],b.prototype,"cache",void 0),b=(0,n.__decorate)([(0,s.EM)("ha-markdown-element")],b)},3587:function(t,e,i){"use strict";i(23792),i(3362),i(62953);var a=i(40445),n=i(96196),o=i(77845);i(69709);let s,r,d=t=>t;class l extends n.WF{async getUpdateComplete(){const t=await super.getUpdateComplete();return await this._markdownElement.updateComplete,t}render(){return this.content?(0,n.qy)(s||(s=d`<ha-markdown-element .content="${0}" .allowSvg="${0}" .allowDataUrl="${0}" .breaks="${0}" .lazyImages="${0}" .cache="${0}"></ha-markdown-element>`),this.content,this.allowSvg,this.allowDataUrl,this.breaks,this.lazyImages,this.cache):n.s6}constructor(...t){super(...t),this.allowSvg=!1,this.allowDataUrl=!1,this.breaks=!1,this.lazyImages=!1,this.cache=!1}}l.styles=(0,n.AH)(r||(r=d`
    :host {
      display: block;
    }
    ha-markdown-element {
      -ms-user-select: text;
      -webkit-user-select: text;
      -moz-user-select: text;
    }
    ha-markdown-element > *:first-child {
      margin-top: 0;
    }
    ha-markdown-element > *:last-child {
      margin-bottom: 0;
    }
    ha-alert {
      display: block;
      margin: var(--ha-space-1) 0;
    }
    a {
      color: var(--markdown-link-color, var(--primary-color));
    }
    img {
      background-color: var(--markdown-image-background-color);
      border-radius: var(--markdown-image-border-radius);
      max-width: 100%;
      height: auto;
      width: auto;
      transition: height 0.2s ease-in-out;
    }
    p:first-child > img:first-child {
      vertical-align: top;
    }
    p:first-child > img:last-child {
      vertical-align: top;
    }
    :host > ul,
    :host > ol {
      padding-inline-start: var(--markdown-list-indent, revert);
    }
    li {
      &:has(input[type="checkbox"]) {
        list-style: none;
        & > input[type="checkbox"] {
          margin-left: 0;
        }
      }
    }
    svg {
      background-color: var(--markdown-svg-background-color, none);
      color: var(--markdown-svg-color, none);
    }
    code,
    pre {
      background-color: var(--markdown-code-background-color, none);
      border-radius: var(--ha-border-radius-sm);
      color: var(--markdown-code-text-color, inherit);
    }
    code {
      font-size: var(--ha-font-size-s);
      padding: 0.2em 0.4em;
    }
    pre code {
      padding: 0;
    }
    pre {
      padding: var(--ha-space-4);
      overflow: auto;
      line-height: var(--ha-line-height-condensed);
      font-family: var(--ha-font-family-code);
    }
    h1,
    h2,
    h3,
    h4,
    h5,
    h6 {
      line-height: initial;
    }
    h2 {
      font-size: var(--ha-font-size-xl);
      font-weight: var(--ha-font-weight-bold);
    }
    hr {
      border-color: var(--divider-color);
      border-bottom: none;
      margin: var(--ha-space-4) 0;
    }
    table {
      border-collapse: var(--markdown-table-border-collapse, collapse);
    }
    div:has(> table) {
      overflow: auto;
    }
    th {
      text-align: start;
    }
    td,
    th {
      border-width: var(--markdown-table-border-width, 1px);
      border-style: var(--markdown-table-border-style, solid);
      border-color: var(--markdown-table-border-color, var(--divider-color));
      padding: 0.25em 0.5em;
    }
    blockquote {
      border-left: 4px solid var(--divider-color);
      margin-inline: 0;
      padding-inline: 1em;
    }
  `)),(0,a.__decorate)([(0,o.MZ)()],l.prototype,"content",void 0),(0,a.__decorate)([(0,o.MZ)({attribute:"allow-svg",type:Boolean})],l.prototype,"allowSvg",void 0),(0,a.__decorate)([(0,o.MZ)({attribute:"allow-data-url",type:Boolean})],l.prototype,"allowDataUrl",void 0),(0,a.__decorate)([(0,o.MZ)({type:Boolean})],l.prototype,"breaks",void 0),(0,a.__decorate)([(0,o.MZ)({type:Boolean,attribute:"lazy-images"})],l.prototype,"lazyImages",void 0),(0,a.__decorate)([(0,o.MZ)({type:Boolean})],l.prototype,"cache",void 0),(0,a.__decorate)([(0,o.P)("ha-markdown-element")],l.prototype,"_markdownElement",void 0),l=(0,a.__decorate)([(0,o.EM)("ha-markdown")],l)},75709:function(t,e,i){"use strict";i.d(e,{h:function(){return g}});i(23792),i(62953);var a=i(40445),n=i(68846),o=i(92347),s=i(96196),r=i(77845),d=i(63091);let l,c,h,p,u=t=>t;class g extends n.J{updated(t){super.updated(t),(t.has("invalid")||t.has("errorMessage"))&&(this.setCustomValidity(this.invalid?this.errorMessage||this.validationMessage||"Invalid":""),(this.invalid||this.validateOnInitialRender||t.has("invalid")&&void 0!==t.get("invalid"))&&this.reportValidity()),t.has("autocomplete")&&(this.autocomplete?this.formElement.setAttribute("autocomplete",this.autocomplete):this.formElement.removeAttribute("autocomplete")),t.has("autocorrect")&&(!1===this.autocorrect?this.formElement.setAttribute("autocorrect","off"):this.formElement.removeAttribute("autocorrect")),t.has("inputSpellcheck")&&(this.inputSpellcheck?this.formElement.setAttribute("spellcheck",this.inputSpellcheck):this.formElement.removeAttribute("spellcheck"))}renderIcon(t,e=!1){const i=e?"trailing":"leading";return(0,s.qy)(l||(l=u` <span class="mdc-text-field__icon mdc-text-field__icon--${0}" tabindex="${0}"> <slot name="${0}Icon"></slot> </span> `),i,e?1:-1,i)}constructor(...t){super(...t),this.icon=!1,this.iconTrailing=!1,this.autocorrect=!0}}g.styles=[o.R,(0,s.AH)(c||(c=u`.mdc-text-field__input{width:var(--ha-textfield-input-width,100%)}.mdc-text-field:not(.mdc-text-field--with-leading-icon){padding:var(--text-field-padding,0px 16px)}.mdc-text-field__affix--suffix{padding-left:var(--text-field-suffix-padding-left,12px);padding-right:var(--text-field-suffix-padding-right,0px);padding-inline-start:var(--text-field-suffix-padding-left,12px);padding-inline-end:var(--text-field-suffix-padding-right,0px);direction:ltr}.mdc-text-field--with-leading-icon{padding-inline-start:var(--text-field-suffix-padding-left,0px);padding-inline-end:var(--text-field-suffix-padding-right,16px);direction:var(--direction)}.mdc-text-field--with-leading-icon.mdc-text-field--with-trailing-icon{padding-left:var(--text-field-suffix-padding-left,0px);padding-right:var(--text-field-suffix-padding-right,0px);padding-inline-start:var(--text-field-suffix-padding-left,0px);padding-inline-end:var(--text-field-suffix-padding-right,0px)}.mdc-text-field:not(.mdc-text-field--disabled) .mdc-text-field__affix--suffix{color:var(--secondary-text-color)}.mdc-text-field:not(.mdc-text-field--disabled) .mdc-text-field__icon{color:var(--secondary-text-color)}.mdc-text-field__icon--leading{margin-inline-start:16px;margin-inline-end:8px;direction:var(--direction)}.mdc-text-field__icon--trailing{padding:var(--textfield-icon-trailing-padding,12px)}.mdc-floating-label:not(.mdc-floating-label--float-above){max-width:calc(100% - 16px)}.mdc-floating-label--float-above{max-width:calc((100% - 16px)/ .75);transition:none}input{text-align:var(--text-field-text-align,start)}input[type=color]{height:20px}::-ms-reveal{display:none}:host([no-spinner]) input::-webkit-inner-spin-button,:host([no-spinner]) input::-webkit-outer-spin-button{-webkit-appearance:none;margin:0}input[type=color]::-webkit-color-swatch-wrapper{padding:0}:host([no-spinner]) input[type=number]{-moz-appearance:textfield}.mdc-text-field__ripple{overflow:hidden}.mdc-text-field{overflow:var(--text-field-overflow)}.mdc-floating-label{padding-inline-end:16px;padding-inline-start:initial;inset-inline-start:16px!important;inset-inline-end:initial!important;transform-origin:var(--float-start);direction:var(--direction);text-align:var(--float-start);box-sizing:border-box;text-overflow:ellipsis}.mdc-text-field--with-leading-icon.mdc-text-field--filled .mdc-floating-label{max-width:calc(100% - 48px - var(--text-field-suffix-padding-left,0px));inset-inline-start:calc(48px + var(--text-field-suffix-padding-left,0px))!important;inset-inline-end:initial!important;direction:var(--direction)}.mdc-text-field__input[type=number]{direction:var(--direction)}.mdc-text-field__affix--prefix{padding-right:var(--text-field-prefix-padding-right,2px);padding-inline-end:var(--text-field-prefix-padding-right,2px);padding-inline-start:initial}.mdc-text-field:not(.mdc-text-field--disabled) .mdc-text-field__affix--prefix{color:var(--mdc-text-field-label-ink-color)}#helper-text ha-markdown{display:inline-block}`)),"rtl"===d.G.document.dir?(0,s.AH)(h||(h=u`.mdc-floating-label,.mdc-text-field--with-leading-icon,.mdc-text-field--with-leading-icon.mdc-text-field--filled .mdc-floating-label,.mdc-text-field__icon--leading,.mdc-text-field__input[type=number]{direction:rtl;--direction:rtl}`)):(0,s.AH)(p||(p=u``))],(0,a.__decorate)([(0,r.MZ)({type:Boolean})],g.prototype,"invalid",void 0),(0,a.__decorate)([(0,r.MZ)({attribute:"error-message"})],g.prototype,"errorMessage",void 0),(0,a.__decorate)([(0,r.MZ)({type:Boolean})],g.prototype,"icon",void 0),(0,a.__decorate)([(0,r.MZ)({type:Boolean})],g.prototype,"iconTrailing",void 0),(0,a.__decorate)([(0,r.MZ)()],g.prototype,"autocomplete",void 0),(0,a.__decorate)([(0,r.MZ)({type:Boolean})],g.prototype,"autocorrect",void 0),(0,a.__decorate)([(0,r.MZ)({attribute:"input-spellcheck"})],g.prototype,"inputSpellcheck",void 0),(0,a.__decorate)([(0,r.P)("input")],g.prototype,"formElement",void 0),g=(0,a.__decorate)([(0,r.EM)("ha-textfield")],g)},69150:function(t,e,i){"use strict";i.d(e,{$$:function(){return _},AH:function(){return n},NH:function(){return p},QC:function(){return a},Uc:function(){return s},Zr:function(){return u},ds:function(){return g},hJ:function(){return r},mp:function(){return l},nx:function(){return d},u6:function(){return c},vU:function(){return o},zn:function(){return h}});i(23792),i(62953);const a=(t,e,i)=>"run-start"===e.type?t={init_options:i,stage:"ready",run:e.data,events:[e],started:new Date(e.timestamp)}:t?((t="wake_word-start"===e.type?Object.assign(Object.assign({},t),{},{stage:"wake_word",wake_word:Object.assign(Object.assign({},e.data),{},{done:!1})}):"wake_word-end"===e.type?Object.assign(Object.assign({},t),{},{wake_word:Object.assign(Object.assign(Object.assign({},t.wake_word),e.data),{},{done:!0})}):"stt-start"===e.type?Object.assign(Object.assign({},t),{},{stage:"stt",stt:Object.assign(Object.assign({},e.data),{},{done:!1})}):"stt-end"===e.type?Object.assign(Object.assign({},t),{},{stt:Object.assign(Object.assign(Object.assign({},t.stt),e.data),{},{done:!0})}):"intent-start"===e.type?Object.assign(Object.assign({},t),{},{stage:"intent",intent:Object.assign(Object.assign({},e.data),{},{done:!1})}):"intent-end"===e.type?Object.assign(Object.assign({},t),{},{intent:Object.assign(Object.assign(Object.assign({},t.intent),e.data),{},{done:!0})}):"tts-start"===e.type?Object.assign(Object.assign({},t),{},{stage:"tts",tts:Object.assign(Object.assign({},e.data),{},{done:!1})}):"tts-end"===e.type?Object.assign(Object.assign({},t),{},{tts:Object.assign(Object.assign(Object.assign({},t.tts),e.data),{},{done:!0})}):"run-end"===e.type?Object.assign(Object.assign({},t),{},{finished:new Date(e.timestamp),stage:"done"}):"error"===e.type?Object.assign(Object.assign({},t),{},{finished:new Date(e.timestamp),stage:"error",error:e.data}):Object.assign({},t)).events=[...t.events,e],t):void console.warn("Received unexpected event before receiving session",e),n=(t,e,i)=>{let n;const s=o(t,t=>{n=a(n,t,i),"run-end"!==t.type&&"error"!==t.type||s.then(t=>t()),n&&e(n)},i);return s},o=(t,e,i)=>t.connection.subscribeMessage(e,Object.assign(Object.assign({},i),{},{type:"assist_pipeline/run"})),s=(t,e)=>t.callWS({type:"assist_pipeline/pipeline_debug/list",pipeline_id:e}),r=(t,e,i)=>t.callWS({type:"assist_pipeline/pipeline_debug/get",pipeline_id:e,pipeline_run_id:i}),d=t=>t.callWS({type:"assist_pipeline/pipeline/list"}),l=(t,e)=>t.callWS({type:"assist_pipeline/pipeline/get",pipeline_id:e}),c=(t,e)=>t.callWS(Object.assign({type:"assist_pipeline/pipeline/create"},e)),h=(t,e,i)=>t.callWS(Object.assign({type:"assist_pipeline/pipeline/update",pipeline_id:e},i)),p=(t,e)=>t.callWS({type:"assist_pipeline/pipeline/set_preferred",pipeline_id:e}),u=(t,e)=>t.callWS({type:"assist_pipeline/pipeline/delete",pipeline_id:e}),g=t=>t.callWS({type:"assist_pipeline/language/list"}),_=t=>t.callWS({type:"assist_pipeline/device/list"})},88433:function(t,e,i){"use strict";if(i.d(e,{RW:function(){return s},ZE:function(){return n},e1:function(){return r},vc:function(){return o}}),59509==i.j)var a=i(44537);var n=function(t){return t[t.CONTROL=1]="CONTROL",t}({});const o=(t,e,i)=>t.callWS({type:"conversation/agent/list",language:e,country:i}),s=(t,e,i,n)=>t.callWS({type:"conversation/agent/homeassistant/debug",sentences:(0,a.e)(e),language:i,device_id:n}),r=(t,e,i)=>t.callWS({type:"conversation/agent/homeassistant/language_scores",language:e,country:i})},74209:function(t,e,i){"use strict";i.d(e,{N:function(){return a}});i(23792),i(3362),i(62953),i(3296),i(27208),i(48408),i(14603),i(47566),i(98721);class a{get active(){return this._active}get sampleRate(){var t;return null===(t=this._context)||void 0===t?void 0:t.sampleRate}static get isSupported(){return window.isSecureContext&&(window.AudioContext||window.webkitAudioContext)}async start(){if(this._context&&this._stream&&this._source&&this._recorder)this._stream.getTracks()[0].enabled=!0,await this._context.resume(),this._active=!0;else try{await this._createContext()}catch(t){console.error(t),this._active=!1}}async stop(){var t;this._active=!1,this._stream&&(this._stream.getTracks()[0].enabled=!1),await(null===(t=this._context)||void 0===t?void 0:t.suspend())}close(){var t,e,i;this._active=!1,null===(t=this._stream)||void 0===t||t.getTracks()[0].stop(),this._recorder&&(this._recorder.port.onmessage=null),null===(e=this._source)||void 0===e||e.disconnect(),null===(i=this._context)||void 0===i||i.close(),this._stream=void 0,this._source=void 0,this._recorder=void 0,this._context=void 0}async _createContext(){const t=new(AudioContext||webkitAudioContext);this._stream=await navigator.mediaDevices.getUserMedia({audio:!0}),await t.audioWorklet.addModule(new URL(i.p+i.u("33921"),i.b)),this._context=t,this._source=this._context.createMediaStreamSource(this._stream),this._recorder=new AudioWorkletNode(this._context,"recorder-worklet"),this._recorder.port.onmessage=t=>{this._active&&this._callback(t.data)},this._active=!0,this._source.connect(this._recorder)}constructor(t){this._active=!1,this._callback=t}}},996:function(t,e,i){"use strict";i.d(e,{G:function(){return a}});i(23792),i(62953);class a{get(t){return this._cache.get(t)}set(t,e){this._cache.set(t,e),this._expiration&&window.setTimeout(()=>this._cache.delete(t),this._expiration)}has(t){return this._cache.has(t)}constructor(t){this._cache=new Map,this._expiration=t}}},36918:function(t,e,i){"use strict";i.d(e,{o:function(){return a}});i(74423);const a=(t,e)=>`https://${t.config.version.includes("b")?"rc":t.config.version.includes("dev")?"next":"www"}.home-assistant.io${e}`},96175:function(t,e,i){var a={"./ha-icon-prev":["89133","61982"],"./ha-icon-button-toolbar":["9882","26431","41983"],"./ha-alert":["38962","19695"],"./ha-icon-button-toggle":["62501","77254"],"./ha-svg-icon.ts":["67094"],"./ha-alert.ts":["38962","19695"],"./ha-icon":["88945","51146"],"./ha-icon-next.ts":["43661","63902"],"./ha-qr-code.ts":["60543","51343","62740"],"./ha-icon-overflow-menu.ts":["75248","46095","26431","22016","17521"],"./ha-icon-button-toggle.ts":["62501","77254"],"./ha-icon-button-group":["39826","13647"],"./ha-svg-icon":["67094"],"./ha-icon-button-prev":["45100","99197"],"./ha-icon-button.ts":["26300"],"./ha-icon-overflow-menu":["75248","46095","26431","22016","17521"],"./ha-icon-button-arrow-next":["99028","54101"],"./ha-icon-button-prev.ts":["45100","99197"],"./ha-icon-picker":["64138","44533","7199","46095","24876","97367","99232"],"./ha-icon-button-toolbar.ts":["9882","26431","41983"],"./ha-icon-button-arrow-prev.ts":["90248","17041"],"./ha-icon-button-next":["3059","81049"],"./ha-icon-next":["43661","63902"],"./ha-icon-picker.ts":["64138","44533","7199","46095","24876","97367","99232"],"./ha-icon-prev.ts":["89133","61982"],"./ha-icon-button-arrow-prev":["90248","17041"],"./ha-icon-button-next.ts":["3059","81049"],"./ha-icon.ts":["88945","51146"],"./ha-qr-code":["60543","51343","62740"],"./ha-icon-button":["26300"],"./ha-icon-button-group.ts":["39826","13647"],"./ha-icon-button-arrow-next.ts":["99028","54101"]};function n(t){if(!i.o(a,t))return Promise.resolve().then(function(){var e=new Error("Cannot find module '"+t+"'");throw e.code="MODULE_NOT_FOUND",e});var e=a[t],n=e[0];return Promise.all(e.slice(1).map(i.e)).then(function(){return i(n)})}n.keys=function(){return Object.keys(a)},n.id=96175,t.exports=n}}]);
//# sourceMappingURL=28845.340ddb19a0bce6d4.js.map