"use strict";(self.webpackChunkhome_assistant_frontend=self.webpackChunkhome_assistant_frontend||[]).push([["78590"],{38962:function(e,t,a){a.r(t);a(23792),a(62953);var o=a(40445),i=a(96196),r=a(77845),s=a(94333),n=a(1087);a(26300),a(67094);let l,d,c,h,p=e=>e;const u={info:"M11,9H13V7H11M12,20C7.59,20 4,16.41 4,12C4,7.59 7.59,4 12,4C16.41,4 20,7.59 20,12C20,16.41 16.41,20 12,20M12,2A10,10 0 0,0 2,12A10,10 0 0,0 12,22A10,10 0 0,0 22,12A10,10 0 0,0 12,2M11,17H13V11H11V17Z",warning:"M12,2L1,21H23M12,6L19.53,19H4.47M11,10V14H13V10M11,16V18H13V16",error:"M11,15H13V17H11V15M11,7H13V13H11V7M12,2C6.47,2 2,6.5 2,12A10,10 0 0,0 12,22A10,10 0 0,0 22,12A10,10 0 0,0 12,2M12,20A8,8 0 0,1 4,12A8,8 0 0,1 12,4A8,8 0 0,1 20,12A8,8 0 0,1 12,20Z",success:"M20,12A8,8 0 0,1 12,20A8,8 0 0,1 4,12A8,8 0 0,1 12,4C12.76,4 13.5,4.11 14.2,4.31L15.77,2.74C14.61,2.26 13.34,2 12,2A10,10 0 0,0 2,12A10,10 0 0,0 12,22A10,10 0 0,0 22,12M7.91,10.08L6.5,11.5L11,16L21,6L19.59,4.58L11,13.17L7.91,10.08Z"};class g extends i.WF{render(){return(0,i.qy)(l||(l=p` <div class="issue-type ${0}" role="alert"> <div class="icon ${0}"> <slot name="icon"> <ha-svg-icon .path="${0}"></ha-svg-icon> </slot> </div> <div class="${0}"> <div class="main-content"> ${0} <slot></slot> </div> <div class="action"> <slot name="action"> ${0} </slot> </div> </div> </div> `),(0,s.H)({[this.alertType]:!0}),this.title?"":"no-title",u[this.alertType],(0,s.H)({content:!0,narrow:this.narrow}),this.title?(0,i.qy)(d||(d=p`<div class="title">${0}</div>`),this.title):i.s6,this.dismissable?(0,i.qy)(c||(c=p`<ha-icon-button @click="${0}" label="Dismiss alert" .path="${0}"></ha-icon-button>`),this._dismissClicked,"M19,6.41L17.59,5L12,10.59L6.41,5L5,6.41L10.59,12L5,17.59L6.41,19L12,13.41L17.59,19L19,17.59L13.41,12L19,6.41Z"):i.s6)}_dismissClicked(){(0,n.r)(this,"alert-dismissed-clicked")}constructor(...e){super(...e),this.title="",this.alertType="info",this.dismissable=!1,this.narrow=!1}}g.styles=(0,i.AH)(h||(h=p`.issue-type{position:relative;padding:8px;display:flex}.icon{height:var(--ha-alert-icon-size,24px);width:var(--ha-alert-icon-size,24px)}.issue-type::after{position:absolute;top:0;right:0;bottom:0;left:0;opacity:.12;pointer-events:none;content:"";border-radius:var(--ha-border-radius-sm)}.icon.no-title{align-self:center}.content{display:flex;justify-content:space-between;align-items:center;width:100%;text-align:var(--float-start)}.content.narrow{flex-direction:column;align-items:flex-end}.action{z-index:1;width:min-content;--mdc-theme-primary:var(--primary-text-color)}.main-content{overflow-wrap:anywhere;word-break:break-word;line-height:normal;margin-left:8px;margin-right:0;margin-inline-start:8px;margin-inline-end:8px}.title{margin-top:2px;font-weight:var(--ha-font-weight-bold)}.action ha-icon-button{--mdc-theme-primary:var(--primary-text-color);--mdc-icon-button-size:36px}.issue-type.info>.icon{color:var(--info-color)}.issue-type.info::after{background-color:var(--info-color)}.issue-type.warning>.icon{color:var(--warning-color)}.issue-type.warning::after{background-color:var(--warning-color)}.issue-type.error>.icon{color:var(--error-color)}.issue-type.error::after{background-color:var(--error-color)}.issue-type.success>.icon{color:var(--success-color)}.issue-type.success::after{background-color:var(--success-color)}:host ::slotted(ul){margin:0;padding-inline-start:20px}`)),(0,o.__decorate)([(0,r.MZ)()],g.prototype,"title",void 0),(0,o.__decorate)([(0,r.MZ)({attribute:"alert-type"})],g.prototype,"alertType",void 0),(0,o.__decorate)([(0,r.MZ)({type:Boolean})],g.prototype,"dismissable",void 0),(0,o.__decorate)([(0,r.MZ)({type:Boolean})],g.prototype,"narrow",void 0),g=(0,o.__decorate)([(0,r.EM)("ha-alert")],g)},76538:function(e,t,a){a(23792),a(62953);var o=a(40445),i=a(96196),r=a(77845);let s,n,l,d,c,h,p=e=>e;class u extends i.WF{render(){const e=(0,i.qy)(s||(s=p`<div class="header-title"> <slot name="title"></slot> </div>`)),t=(0,i.qy)(n||(n=p`<div class="header-subtitle"> <slot name="subtitle"></slot> </div>`));return(0,i.qy)(l||(l=p` <header class="header"> <div class="header-bar"> <section class="header-navigation-icon"> <slot name="navigationIcon"></slot> </section> <section class="header-content"> ${0} </section> <section class="header-action-items"> <slot name="actionItems"></slot> </section> </div> <slot></slot> </header> `),"above"===this.subtitlePosition?(0,i.qy)(d||(d=p`${0}${0}`),t,e):(0,i.qy)(c||(c=p`${0}${0}`),e,t))}static get styles(){return[(0,i.AH)(h||(h=p`:host{display:block}:host([show-border]){border-bottom:1px solid var(--mdc-dialog-scroll-divider-color,rgba(0,0,0,.12))}.header-bar{display:flex;flex-direction:row;align-items:center;padding:0 var(--ha-space-1);box-sizing:border-box}.header-content{flex:1;padding:10px var(--ha-space-1);display:flex;flex-direction:column;justify-content:center;min-height:var(--ha-space-12);min-width:0;overflow:hidden;text-overflow:ellipsis;white-space:nowrap}.header-title{height:var(--ha-dialog-header-title-height,calc(var(--ha-font-size-xl) + var(--ha-space-1)));font-size:var(--ha-font-size-xl);line-height:var(--ha-line-height-condensed);font-weight:var(--ha-font-weight-medium);color:var(--ha-dialog-header-title-color,var(--primary-text-color))}.header-subtitle{font-size:var(--ha-font-size-m);line-height:var(--ha-line-height-normal);color:var(--ha-dialog-header-subtitle-color,var(--secondary-text-color))}@media all and (min-width:450px) and (min-height:500px){.header-bar{padding:0 var(--ha-space-2)}}.header-navigation-icon{flex:none;min-width:var(--ha-space-2);height:100%;display:flex;flex-direction:row}.header-action-items{flex:none;min-width:var(--ha-space-2);height:100%;display:flex;flex-direction:row}`))]}constructor(...e){super(...e),this.subtitlePosition="below",this.showBorder=!1}}(0,o.__decorate)([(0,r.MZ)({type:String,attribute:"subtitle-position"})],u.prototype,"subtitlePosition",void 0),(0,o.__decorate)([(0,r.MZ)({type:Boolean,reflect:!0,attribute:"show-border"})],u.prototype,"showBorder",void 0),u=(0,o.__decorate)([(0,r.EM)("ha-dialog-header")],u)},45331:function(e,t,a){a.a(e,async function(e,t){try{a(23792),a(3362),a(62953);var o=a(40445),i=a(93900),r=a(96196),s=a(77845),n=a(32288),l=a(1087),d=a(14503),c=(a(76538),a(26300),e([i]));i=(c.then?(await c)():c)[0];let h,p,u,g,f,v,w=e=>e;const m="M19,6.41L17.59,5L12,10.59L6.41,5L5,6.41L10.59,12L5,17.59L6.41,19L12,13.41L17.59,19L19,17.59L13.41,12L19,6.41Z";class b extends r.WF{updated(e){super.updated(e),e.has("open")&&(this._open=this.open)}render(){var e,t;return(0,r.qy)(h||(h=w` <wa-dialog .open="${0}" .lightDismiss="${0}" without-header aria-labelledby="${0}" aria-describedby="${0}" @wa-show="${0}" @wa-after-show="${0}" @wa-after-hide="${0}"> <slot name="header"> <ha-dialog-header .subtitlePosition="${0}" .showBorder="${0}"> <slot name="headerNavigationIcon" slot="navigationIcon"> <ha-icon-button data-dialog="close" .label="${0}" .path="${0}"></ha-icon-button> </slot> ${0} ${0} <slot name="headerActionItems" slot="actionItems"></slot> </ha-dialog-header> </slot> <div class="body ha-scrollbar" @scroll="${0}"> <slot></slot> </div> <slot name="footer" slot="footer"></slot> </wa-dialog> `),this._open,!this.preventScrimClose,(0,n.J)(this.ariaLabelledBy||(void 0!==this.headerTitle?"ha-wa-dialog-title":void 0)),(0,n.J)(this.ariaDescribedBy),this._handleShow,this._handleAfterShow,this._handleAfterHide,this.headerSubtitlePosition,this._bodyScrolled,null!==(e=null===(t=this.hass)||void 0===t?void 0:t.localize("ui.common.close"))&&void 0!==e?e:"Close",m,void 0!==this.headerTitle?(0,r.qy)(p||(p=w`<span slot="title" class="title" id="ha-wa-dialog-title"> ${0} </span>`),this.headerTitle):(0,r.qy)(u||(u=w`<slot name="headerTitle" slot="title"></slot>`)),void 0!==this.headerSubtitle?(0,r.qy)(g||(g=w`<span slot="subtitle">${0}</span>`),this.headerSubtitle):(0,r.qy)(f||(f=w`<slot name="headerSubtitle" slot="subtitle"></slot>`)),this._handleBodyScroll)}disconnectedCallback(){super.disconnectedCallback(),this._open=!1}_handleBodyScroll(e){this._bodyScrolled=e.target.scrollTop>0}constructor(...e){super(...e),this.open=!1,this.type="standard",this.width="medium",this.preventScrimClose=!1,this.headerSubtitlePosition="below",this.flexContent=!1,this._open=!1,this._bodyScrolled=!1,this._handleShow=async()=>{this._open=!0,(0,l.r)(this,"opened"),await this.updateComplete,requestAnimationFrame(()=>{var e;null===(e=this.querySelector("[autofocus]"))||void 0===e||e.focus()})},this._handleAfterShow=()=>{(0,l.r)(this,"after-show")},this._handleAfterHide=()=>{this._open=!1,(0,l.r)(this,"closed")}}}b.styles=[d.dp,(0,r.AH)(v||(v=w`
      wa-dialog {
        --full-width: var(--ha-dialog-width-full, min(95vw, var(--safe-width)));
        --width: min(var(--ha-dialog-width-md, 580px), var(--full-width));
        --spacing: var(--dialog-content-padding, var(--ha-space-6));
        --show-duration: var(--ha-dialog-show-duration, 200ms);
        --hide-duration: var(--ha-dialog-hide-duration, 200ms);
        --ha-dialog-surface-background: var(
          --card-background-color,
          var(--ha-color-surface-default)
        );
        --wa-color-surface-raised: var(
          --ha-dialog-surface-background,
          var(--card-background-color, var(--ha-color-surface-default))
        );
        --wa-panel-border-radius: var(
          --ha-dialog-border-radius,
          var(--ha-border-radius-3xl)
        );
        max-width: var(--ha-dialog-max-width, var(--safe-width));
      }

      :host([width="small"]) wa-dialog {
        --width: min(var(--ha-dialog-width-sm, 320px), var(--full-width));
      }

      :host([width="large"]) wa-dialog {
        --width: min(var(--ha-dialog-width-lg, 1024px), var(--full-width));
      }

      :host([width="full"]) wa-dialog {
        --width: var(--full-width);
      }

      wa-dialog::part(dialog) {
        min-width: var(--width, var(--full-width));
        max-width: var(--width, var(--full-width));
        max-height: var(
          --ha-dialog-max-height,
          calc(var(--safe-height) - var(--ha-space-20))
        );
        min-height: var(--ha-dialog-min-height);
        margin-top: var(--dialog-surface-margin-top, auto);
        /* Used to offset the dialog from the safe areas when space is limited */
        transform: translate(
          calc(
            var(--safe-area-offset-left, var(--ha-space-0)) - var(
                --safe-area-offset-right,
                var(--ha-space-0)
              )
          ),
          calc(
            var(--safe-area-offset-top, var(--ha-space-0)) - var(
                --safe-area-offset-bottom,
                var(--ha-space-0)
              )
          )
        );
        display: flex;
        flex-direction: column;
        overflow: hidden;
      }

      @media all and (max-width: 450px), all and (max-height: 500px) {
        :host([type="standard"]) {
          --ha-dialog-border-radius: var(--ha-space-0);

          wa-dialog {
            /* Make the container fill the whole screen width and not the safe width */
            --full-width: var(--ha-dialog-width-full, 100vw);
            --width: var(--full-width);
          }

          wa-dialog::part(dialog) {
            /* Make the dialog fill the whole screen height and not the safe height */
            min-height: var(--ha-dialog-min-height, 100vh);
            min-height: var(--ha-dialog-min-height, 100dvh);
            max-height: var(--ha-dialog-max-height, 100vh);
            max-height: var(--ha-dialog-max-height, 100dvh);
            margin-top: 0;
            margin-bottom: 0;
            /* Use safe area as padding instead of the container size */
            padding-top: var(--safe-area-inset-top);
            padding-bottom: var(--safe-area-inset-bottom);
            padding-left: var(--safe-area-inset-left);
            padding-right: var(--safe-area-inset-right);
            /* Reset the transform to center the dialog */
            transform: none;
          }
        }
      }

      .header-title-container {
        display: flex;
        align-items: center;
      }

      .header-title {
        margin: 0;
        margin-bottom: 0;
        color: var(--ha-dialog-header-title-color, var(--primary-text-color));
        font-size: var(
          --ha-dialog-header-title-font-size,
          var(--ha-font-size-2xl)
        );
        line-height: var(
          --ha-dialog-header-title-line-height,
          var(--ha-line-height-condensed)
        );
        font-weight: var(
          --ha-dialog-header-title-font-weight,
          var(--ha-font-weight-normal)
        );
        overflow: hidden;
        text-overflow: ellipsis;
        white-space: nowrap;
        margin-right: var(--ha-space-3);
      }

      wa-dialog::part(body) {
        padding: 0;
        display: flex;
        flex-direction: column;
        max-width: 100%;
        overflow: hidden;
      }

      .body {
        position: var(--dialog-content-position, relative);
        padding: 0 var(--dialog-content-padding, var(--ha-space-6))
          var(--dialog-content-padding, var(--ha-space-6))
          var(--dialog-content-padding, var(--ha-space-6));
        overflow: auto;
        flex-grow: 1;
      }
      :host([flexcontent]) .body {
        max-width: 100%;
        flex: 1;
        display: flex;
        flex-direction: column;
      }

      wa-dialog::part(footer) {
        padding: var(--ha-space-0);
      }

      ::slotted([slot="footer"]) {
        display: flex;
        padding: var(--ha-space-3) var(--ha-space-4) var(--ha-space-4)
          var(--ha-space-4);
        gap: var(--ha-space-3);
        justify-content: flex-end;
        align-items: center;
        width: 100%;
      }
    `))],(0,o.__decorate)([(0,s.MZ)({attribute:!1})],b.prototype,"hass",void 0),(0,o.__decorate)([(0,s.MZ)({attribute:"aria-labelledby"})],b.prototype,"ariaLabelledBy",void 0),(0,o.__decorate)([(0,s.MZ)({attribute:"aria-describedby"})],b.prototype,"ariaDescribedBy",void 0),(0,o.__decorate)([(0,s.MZ)({type:Boolean,reflect:!0})],b.prototype,"open",void 0),(0,o.__decorate)([(0,s.MZ)({reflect:!0})],b.prototype,"type",void 0),(0,o.__decorate)([(0,s.MZ)({type:String,reflect:!0,attribute:"width"})],b.prototype,"width",void 0),(0,o.__decorate)([(0,s.MZ)({type:Boolean,reflect:!0,attribute:"prevent-scrim-close"})],b.prototype,"preventScrimClose",void 0),(0,o.__decorate)([(0,s.MZ)({attribute:"header-title"})],b.prototype,"headerTitle",void 0),(0,o.__decorate)([(0,s.MZ)({attribute:"header-subtitle"})],b.prototype,"headerSubtitle",void 0),(0,o.__decorate)([(0,s.MZ)({type:String,attribute:"header-subtitle-position"})],b.prototype,"headerSubtitlePosition",void 0),(0,o.__decorate)([(0,s.MZ)({type:Boolean,reflect:!0,attribute:"flexcontent"})],b.prototype,"flexContent",void 0),(0,o.__decorate)([(0,s.wk)()],b.prototype,"_open",void 0),(0,o.__decorate)([(0,s.P)(".body")],b.prototype,"bodyContainer",void 0),(0,o.__decorate)([(0,s.wk)()],b.prototype,"_bodyScrolled",void 0),(0,o.__decorate)([(0,s.Ls)({passive:!0})],b.prototype,"_handleBodyScroll",null),b=(0,o.__decorate)([(0,s.EM)("ha-wa-dialog")],b),t()}catch(h){t(h)}})},30884:function(e,t,a){a.d(t,{A:function(){return o},K:function(){return i}});const o=(e,t,a)=>e.connection.subscribeMessage(t,{type:"backup/subscribe_events"},{preCheck:a}),i={manager_state:"idle"}},25069:function(e,t,a){a.a(e,async function(e,o){try{a.r(t);a(23792),a(3362),a(62953);var i=a(40445),r=a(96196),s=a(77845),n=a(1087),l=(a(38962),a(45331)),d=a(65829),c=a(30884),h=a(14503),p=e([l,d]);[l,d]=p.then?(await p)():p;let u,g,f,v,w=e=>e;class m extends r.WF{async showDialog(e){this._open=!0,this._loadBackupState(),this._title=e.title,this._backupState=e.initialBackupState,this._actionOnIdle=e.action}closeDialog(){this._open=!1}_dialogClosed(){this._backupEventsSubscription&&(this._backupEventsSubscription.then(e=>{e()}),this._backupEventsSubscription=void 0),(0,n.r)(this,"dialog-closed",{dialog:this.localName})}_getWaitMessage(){switch(this._backupState){case"create_backup":return this.hass.localize("ui.dialogs.restart.wait_for_backup");case"receive_backup":return this.hass.localize("ui.dialogs.restart.wait_for_upload");case"restore_backup":return this.hass.localize("ui.dialogs.restart.wait_for_restore");default:return""}}render(){const e=this._getWaitMessage();return(0,r.qy)(u||(u=w` <ha-wa-dialog .hass="${0}" .open="${0}" .headerTitle="${0}" width="medium" @closed="${0}"> <div class="content"> ${0} </div> </ha-wa-dialog> `),this.hass,this._open,this._title,this._dialogClosed,this._error?(0,r.qy)(g||(g=w`<ha-alert alert-type="error">${0}</ha-alert> `),this.hass.localize("ui.dialogs.restart.error_backup_state",{error:this._error})):(0,r.qy)(f||(f=w` <ha-spinner></ha-spinner> ${0} `),e))}async _loadBackupState(){try{this._backupEventsSubscription=(0,c.A)(this.hass,async e=>{var t;(this._backupState=e.manager_state,"idle"===this._backupState)&&(this.closeDialog(),await(null===(t=this._actionOnIdle)||void 0===t?void 0:t.call(this)))})}catch(e){this._error=e.message||e}}static get styles(){return[h.RF,h.nA,(0,r.AH)(v||(v=w`ha-wa-dialog{--dialog-content-padding:0}.content{display:flex;flex-direction:column;align-items:center;padding:24px;gap:32px}`))]}constructor(...e){super(...e),this._open=!1,this._title=""}}(0,i.__decorate)([(0,s.MZ)({attribute:!1})],m.prototype,"hass",void 0),(0,i.__decorate)([(0,s.wk)()],m.prototype,"_open",void 0),(0,i.__decorate)([(0,s.wk)()],m.prototype,"_title",void 0),(0,i.__decorate)([(0,s.wk)()],m.prototype,"_error",void 0),(0,i.__decorate)([(0,s.wk)()],m.prototype,"_backupState",void 0),m=(0,i.__decorate)([(0,s.EM)("dialog-restart-wait")],m),o()}catch(u){o(u)}})},99793:function(e,t,a){var o=a(96196);let i;t.A=(0,o.AH)(i||(i=(e=>e)`:host{--width:31rem;--spacing:var(--wa-space-l);--show-duration:200ms;--hide-duration:200ms;display:none}:host([open]){display:block}.dialog{display:flex;flex-direction:column;top:0;right:0;bottom:0;left:0;width:var(--width);max-width:calc(100% - var(--wa-space-2xl));max-height:calc(100% - var(--wa-space-2xl));background-color:var(--wa-color-surface-raised);border-radius:var(--wa-panel-border-radius);border:none;box-shadow:var(--wa-shadow-l);padding:0;margin:auto}.dialog.show{animation:show-dialog var(--show-duration) ease}.dialog.show::backdrop{animation:show-backdrop var(--show-duration,200ms) ease}.dialog.hide{animation:show-dialog var(--hide-duration) ease reverse}.dialog.hide::backdrop{animation:show-backdrop var(--hide-duration,200ms) ease reverse}.dialog.pulse{animation:pulse 250ms ease}.dialog:focus{outline:0}@media screen and (max-width:420px){.dialog{max-height:80vh}}.open{display:flex;opacity:1}.header{flex:0 0 auto;display:flex;flex-wrap:nowrap;padding-inline-start:var(--spacing);padding-block-end:0;padding-inline-end:calc(var(--spacing) - var(--wa-form-control-padding-block));padding-block-start:calc(var(--spacing) - var(--wa-form-control-padding-block))}.title{align-self:center;flex:1 1 auto;font-family:inherit;font-size:var(--wa-font-size-l);font-weight:var(--wa-font-weight-heading);line-height:var(--wa-line-height-condensed);margin:0}.header-actions{align-self:start;display:flex;flex-shrink:0;flex-wrap:wrap;justify-content:end;gap:var(--wa-space-2xs);padding-inline-start:var(--spacing)}.header-actions ::slotted(wa-button),.header-actions wa-button{flex:0 0 auto;display:flex;align-items:center}.body{flex:1 1 auto;display:block;padding:var(--spacing);overflow:auto;-webkit-overflow-scrolling:touch}.body:focus{outline:0}.body:focus-visible{outline:var(--wa-focus-ring);outline-offset:var(--wa-focus-ring-offset)}.footer{flex:0 0 auto;display:flex;flex-wrap:wrap;gap:var(--wa-space-xs);justify-content:end;padding:var(--spacing);padding-block-start:0}.footer ::slotted(wa-button:not(:first-of-type)){margin-inline-start:var(--wa-spacing-xs)}.dialog::backdrop{background-color:var(--wa-color-overlay-modal,rgb(0 0 0 / .25))}@keyframes pulse{0%{scale:1}50%{scale:1.02}100%{scale:1}}@keyframes show-dialog{from{opacity:0;scale:0.8}to{opacity:1;scale:1}}@keyframes show-backdrop{from{opacity:0}to{opacity:1}}@media (forced-colors:active){.dialog{border:solid 1px #fff}}`))},93900:function(e,t,a){a.a(e,async function(e,t){try{a(23792),a(3362),a(27495),a(62953);var o=a(96196),i=a(77845),r=a(94333),s=a(32288),n=a(17051),l=a(42462),d=a(28438),c=a(98779),h=a(27259),p=a(31247),u=a(97039),g=a(92070),f=a(9395),v=a(32510),w=a(17060),m=a(88496),b=a(99793),y=e([m,w]);[m,w]=y.then?(await y)():y;let L,M,C,$=e=>e;var _=Object.defineProperty,x=Object.getOwnPropertyDescriptor,k=(e,t,a,o)=>{for(var i,r=o>1?void 0:o?x(t,a):t,s=e.length-1;s>=0;s--)(i=e[s])&&(r=(o?i(t,a,r):i(r))||r);return o&&r&&_(t,a,r),r};let S=class extends v.A{firstUpdated(){this.open&&(this.addOpenListeners(),this.dialog.showModal(),(0,u.JG)(this))}disconnectedCallback(){super.disconnectedCallback(),(0,u.I7)(this),this.removeOpenListeners()}async requestClose(e){const t=new d.L({source:e});if(this.dispatchEvent(t),t.defaultPrevented)return this.open=!0,void(0,h.Ud)(this.dialog,"pulse");this.removeOpenListeners(),await(0,h.Ud)(this.dialog,"hide"),this.open=!1,this.dialog.close(),(0,u.I7)(this);const a=this.originalTrigger;"function"==typeof(null==a?void 0:a.focus)&&setTimeout(()=>a.focus()),this.dispatchEvent(new n.Z)}addOpenListeners(){document.addEventListener("keydown",this.handleDocumentKeyDown)}removeOpenListeners(){document.removeEventListener("keydown",this.handleDocumentKeyDown)}handleDialogCancel(e){e.preventDefault(),this.dialog.classList.contains("hide")||e.target!==this.dialog||this.requestClose(this.dialog)}handleDialogClick(e){const t=e.target.closest('[data-dialog="close"]');t&&(e.stopPropagation(),this.requestClose(t))}async handleDialogPointerDown(e){e.target===this.dialog&&(this.lightDismiss?this.requestClose(this.dialog):await(0,h.Ud)(this.dialog,"pulse"))}handleOpenChange(){this.open&&!this.dialog.open?this.show():!this.open&&this.dialog.open&&(this.open=!0,this.requestClose(this.dialog))}async show(){const e=new c.k;this.dispatchEvent(e),e.defaultPrevented?this.open=!1:(this.addOpenListeners(),this.originalTrigger=document.activeElement,this.open=!0,this.dialog.showModal(),(0,u.JG)(this),requestAnimationFrame(()=>{const e=this.querySelector("[autofocus]");e&&"function"==typeof e.focus?e.focus():this.dialog.focus()}),await(0,h.Ud)(this.dialog,"show"),this.dispatchEvent(new l.q))}render(){var e;const t=!this.withoutHeader,a=this.hasSlotController.test("footer");return(0,o.qy)(L||(L=$` <dialog aria-labelledby="${0}" aria-describedby="${0}" part="dialog" class="${0}" @cancel="${0}" @click="${0}" @pointerdown="${0}"> ${0} <div part="body" class="body"><slot></slot></div> ${0} </dialog> `),null!==(e=this.ariaLabelledby)&&void 0!==e?e:"title",(0,s.J)(this.ariaDescribedby),(0,r.H)({dialog:!0,open:this.open}),this.handleDialogCancel,this.handleDialogClick,this.handleDialogPointerDown,t?(0,o.qy)(M||(M=$` <header part="header" class="header"> <h2 part="title" class="title" id="title"> <slot name="label"> ${0} </slot> </h2> <div part="header-actions" class="header-actions"> <slot name="header-actions"></slot> <wa-button part="close-button" exportparts="base:close-button__base" class="close" appearance="plain" @click="${0}"> <wa-icon name="xmark" label="${0}" library="system" variant="solid"></wa-icon> </wa-button> </div> </header> `),this.label.length>0?this.label:String.fromCharCode(8203),e=>this.requestClose(e.target),this.localize.term("close")):"",a?(0,o.qy)(C||(C=$` <footer part="footer" class="footer"> <slot name="footer"></slot> </footer> `)):"")}constructor(){super(...arguments),this.localize=new w.c(this),this.hasSlotController=new g.X(this,"footer","header-actions","label"),this.open=!1,this.label="",this.withoutHeader=!1,this.lightDismiss=!1,this.handleDocumentKeyDown=e=>{"Escape"===e.key&&this.open&&(e.preventDefault(),e.stopPropagation(),this.requestClose(this.dialog))}}};S.css=b.A,k([(0,i.P)(".dialog")],S.prototype,"dialog",2),k([(0,i.MZ)({type:Boolean,reflect:!0})],S.prototype,"open",2),k([(0,i.MZ)({reflect:!0})],S.prototype,"label",2),k([(0,i.MZ)({attribute:"without-header",type:Boolean,reflect:!0})],S.prototype,"withoutHeader",2),k([(0,i.MZ)({attribute:"light-dismiss",type:Boolean})],S.prototype,"lightDismiss",2),k([(0,i.MZ)({attribute:"aria-labelledby"})],S.prototype,"ariaLabelledby",2),k([(0,i.MZ)({attribute:"aria-describedby"})],S.prototype,"ariaDescribedby",2),k([(0,f.w)("open",{waitUntilFirstUpdate:!0})],S.prototype,"handleOpenChange",1),S=k([(0,i.EM)("wa-dialog")],S),document.addEventListener("click",e=>{const t=e.target.closest("[data-dialog]");if(t instanceof Element){const[e,a]=(0,p.v)(t.getAttribute("data-dialog")||"");if("open"===e&&null!=a&&a.length){const e=t.getRootNode().getElementById(a);"wa-dialog"===(null==e?void 0:e.localName)?e.open=!0:console.warn(`A dialog with an ID of "${a}" could not be found in this document.`)}}}),o.S$||document.addEventListener("pointerdown",()=>{}),t()}catch(L){t(L)}})},17051:function(e,t,a){a.d(t,{Z:function(){return o}});class o extends Event{constructor(){super("wa-after-hide",{bubbles:!0,cancelable:!1,composed:!0})}}},42462:function(e,t,a){a.d(t,{q:function(){return o}});class o extends Event{constructor(){super("wa-after-show",{bubbles:!0,cancelable:!1,composed:!0})}}},28438:function(e,t,a){a.d(t,{L:function(){return o}});class o extends Event{constructor(e){super("wa-hide",{bubbles:!0,cancelable:!0,composed:!0}),this.detail=e}}},98779:function(e,t,a){a.d(t,{k:function(){return o}});class o extends Event{constructor(){super("wa-show",{bubbles:!0,cancelable:!0,composed:!0})}}},27259:function(e,t,a){a.d(t,{E9:function(){return r},Ud:function(){return i},i0:function(){return o}});a(3362);async function o(e,t,a){return e.animate(t,a).finished.catch(()=>{})}function i(e,t){return new Promise(a=>{const o=new AbortController,{signal:i}=o;if(e.classList.contains(t))return;e.classList.remove(t),e.classList.add(t);let r=()=>{e.classList.remove(t),a(),o.abort()};e.addEventListener("animationend",r,{once:!0,signal:i}),e.addEventListener("animationcancel",r,{once:!0,signal:i})})}function r(e){return(e=e.toString().toLowerCase()).indexOf("ms")>-1?parseFloat(e)||0:e.indexOf("s")>-1?1e3*(parseFloat(e)||0):parseFloat(e)||0}},91081:function(e,t,a){function o(e,t){return{top:Math.round(e.getBoundingClientRect().top-t.getBoundingClientRect().top),left:Math.round(e.getBoundingClientRect().left-t.getBoundingClientRect().left)}}a.d(t,{A:function(){return o}})},31247:function(e,t,a){a.d(t,{v:function(){return o}});a(18111),a(22489),a(61701),a(42762);function o(e){return e.split(" ").map(e=>e.trim()).filter(e=>""!==e)}},97039:function(e,t,a){a.d(t,{I7:function(){return s},JG:function(){return r},Rt:function(){return n}});a(23792),a(27495),a(17642),a(58004),a(33853),a(45876),a(32475),a(15024),a(31698),a(25440),a(62953);var o=a(91081);const i=new Set;function r(e){if(i.add(e),!document.documentElement.classList.contains("wa-scroll-lock")){const e=function(){const e=document.documentElement.clientWidth;return Math.abs(window.innerWidth-e)}()+function(){const e=Number(getComputedStyle(document.body).paddingRight.replace(/px/,""));return isNaN(e)||!e?0:e}();let t=getComputedStyle(document.documentElement).scrollbarGutter;t&&"auto"!==t||(t="stable"),e<2&&(t=""),document.documentElement.style.setProperty("--wa-scroll-lock-gutter",t),document.documentElement.classList.add("wa-scroll-lock"),document.documentElement.style.setProperty("--wa-scroll-lock-size",`${e}px`)}}function s(e){i.delete(e),0===i.size&&(document.documentElement.classList.remove("wa-scroll-lock"),document.documentElement.style.removeProperty("--wa-scroll-lock-size"))}function n(e,t,a="vertical",i="smooth"){const r=(0,o.A)(e,t),s=r.top+t.scrollTop,n=r.left+t.scrollLeft,l=t.scrollLeft,d=t.scrollLeft+t.offsetWidth,c=t.scrollTop,h=t.scrollTop+t.offsetHeight;"horizontal"!==a&&"both"!==a||(n<l?t.scrollTo({left:n,behavior:i}):n+e.clientWidth>d&&t.scrollTo({left:n-t.offsetWidth+e.clientWidth,behavior:i})),"vertical"!==a&&"both"!==a||(s<c?t.scrollTo({top:s,behavior:i}):s+e.clientHeight>h&&t.scrollTo({top:s-t.offsetHeight+e.clientHeight,behavior:i}))}}}]);
//# sourceMappingURL=78590.22a15dc38a8a0be8.js.map