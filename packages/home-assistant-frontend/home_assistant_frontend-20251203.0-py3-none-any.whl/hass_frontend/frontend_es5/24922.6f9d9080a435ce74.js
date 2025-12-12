"use strict";(self.webpackChunkhome_assistant_frontend=self.webpackChunkhome_assistant_frontend||[]).push([["24922"],{93444:function(e,t,a){var o=a(40445),i=a(96196),s=a(77845);let r,l,n=e=>e;class d extends i.WF{render(){return(0,i.qy)(r||(r=n` <footer> <slot name="secondaryAction"></slot> <slot name="primaryAction"></slot> </footer> `))}static get styles(){return[(0,i.AH)(l||(l=n`footer{display:flex;gap:var(--ha-space-3);justify-content:flex-end;align-items:center;width:100%}`))]}}d=(0,o.__decorate)([(0,s.EM)("ha-dialog-footer")],d)},76538:function(e,t,a){a(23792),a(62953);var o=a(40445),i=a(96196),s=a(77845);let r,l,n,d,h,c,p=e=>e;class g extends i.WF{render(){const e=(0,i.qy)(r||(r=p`<div class="header-title"> <slot name="title"></slot> </div>`)),t=(0,i.qy)(l||(l=p`<div class="header-subtitle"> <slot name="subtitle"></slot> </div>`));return(0,i.qy)(n||(n=p` <header class="header"> <div class="header-bar"> <section class="header-navigation-icon"> <slot name="navigationIcon"></slot> </section> <section class="header-content"> ${0} </section> <section class="header-action-items"> <slot name="actionItems"></slot> </section> </div> <slot></slot> </header> `),"above"===this.subtitlePosition?(0,i.qy)(d||(d=p`${0}${0}`),t,e):(0,i.qy)(h||(h=p`${0}${0}`),e,t))}static get styles(){return[(0,i.AH)(c||(c=p`:host{display:block}:host([show-border]){border-bottom:1px solid var(--mdc-dialog-scroll-divider-color,rgba(0,0,0,.12))}.header-bar{display:flex;flex-direction:row;align-items:center;padding:0 var(--ha-space-1);box-sizing:border-box}.header-content{flex:1;padding:10px var(--ha-space-1);display:flex;flex-direction:column;justify-content:center;min-height:var(--ha-space-12);min-width:0;overflow:hidden;text-overflow:ellipsis;white-space:nowrap}.header-title{height:var(--ha-dialog-header-title-height,calc(var(--ha-font-size-xl) + var(--ha-space-1)));font-size:var(--ha-font-size-xl);line-height:var(--ha-line-height-condensed);font-weight:var(--ha-font-weight-medium);color:var(--ha-dialog-header-title-color,var(--primary-text-color))}.header-subtitle{font-size:var(--ha-font-size-m);line-height:var(--ha-line-height-normal);color:var(--ha-dialog-header-subtitle-color,var(--secondary-text-color))}@media all and (min-width:450px) and (min-height:500px){.header-bar{padding:0 var(--ha-space-2)}}.header-navigation-icon{flex:none;min-width:var(--ha-space-2);height:100%;display:flex;flex-direction:row}.header-action-items{flex:none;min-width:var(--ha-space-2);height:100%;display:flex;flex-direction:row}`))]}constructor(...e){super(...e),this.subtitlePosition="below",this.showBorder=!1}}(0,o.__decorate)([(0,s.MZ)({type:String,attribute:"subtitle-position"})],g.prototype,"subtitlePosition",void 0),(0,o.__decorate)([(0,s.MZ)({type:Boolean,reflect:!0,attribute:"show-border"})],g.prototype,"showBorder",void 0),g=(0,o.__decorate)([(0,s.EM)("ha-dialog-header")],g)},45331:function(e,t,a){a.a(e,async function(e,t){try{a(23792),a(3362),a(62953);var o=a(40445),i=a(93900),s=a(96196),r=a(77845),l=a(32288),n=a(1087),d=a(14503),h=(a(76538),a(26300),e([i]));i=(h.then?(await h)():h)[0];let c,p,g,u,f,v,m=e=>e;const w="M19,6.41L17.59,5L12,10.59L6.41,5L5,6.41L10.59,12L5,17.59L6.41,19L12,13.41L17.59,19L19,17.59L13.41,12L19,6.41Z";class b extends s.WF{updated(e){super.updated(e),e.has("open")&&(this._open=this.open)}render(){var e,t;return(0,s.qy)(c||(c=m` <wa-dialog .open="${0}" .lightDismiss="${0}" without-header aria-labelledby="${0}" aria-describedby="${0}" @wa-show="${0}" @wa-after-show="${0}" @wa-after-hide="${0}"> <slot name="header"> <ha-dialog-header .subtitlePosition="${0}" .showBorder="${0}"> <slot name="headerNavigationIcon" slot="navigationIcon"> <ha-icon-button data-dialog="close" .label="${0}" .path="${0}"></ha-icon-button> </slot> ${0} ${0} <slot name="headerActionItems" slot="actionItems"></slot> </ha-dialog-header> </slot> <div class="body ha-scrollbar" @scroll="${0}"> <slot></slot> </div> <slot name="footer" slot="footer"></slot> </wa-dialog> `),this._open,!this.preventScrimClose,(0,l.J)(this.ariaLabelledBy||(void 0!==this.headerTitle?"ha-wa-dialog-title":void 0)),(0,l.J)(this.ariaDescribedBy),this._handleShow,this._handleAfterShow,this._handleAfterHide,this.headerSubtitlePosition,this._bodyScrolled,null!==(e=null===(t=this.hass)||void 0===t?void 0:t.localize("ui.common.close"))&&void 0!==e?e:"Close",w,void 0!==this.headerTitle?(0,s.qy)(p||(p=m`<span slot="title" class="title" id="ha-wa-dialog-title"> ${0} </span>`),this.headerTitle):(0,s.qy)(g||(g=m`<slot name="headerTitle" slot="title"></slot>`)),void 0!==this.headerSubtitle?(0,s.qy)(u||(u=m`<span slot="subtitle">${0}</span>`),this.headerSubtitle):(0,s.qy)(f||(f=m`<slot name="headerSubtitle" slot="subtitle"></slot>`)),this._handleBodyScroll)}disconnectedCallback(){super.disconnectedCallback(),this._open=!1}_handleBodyScroll(e){this._bodyScrolled=e.target.scrollTop>0}constructor(...e){super(...e),this.open=!1,this.type="standard",this.width="medium",this.preventScrimClose=!1,this.headerSubtitlePosition="below",this.flexContent=!1,this._open=!1,this._bodyScrolled=!1,this._handleShow=async()=>{this._open=!0,(0,n.r)(this,"opened"),await this.updateComplete,requestAnimationFrame(()=>{var e;null===(e=this.querySelector("[autofocus]"))||void 0===e||e.focus()})},this._handleAfterShow=()=>{(0,n.r)(this,"after-show")},this._handleAfterHide=()=>{this._open=!1,(0,n.r)(this,"closed")}}}b.styles=[d.dp,(0,s.AH)(v||(v=m`
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
    `))],(0,o.__decorate)([(0,r.MZ)({attribute:!1})],b.prototype,"hass",void 0),(0,o.__decorate)([(0,r.MZ)({attribute:"aria-labelledby"})],b.prototype,"ariaLabelledBy",void 0),(0,o.__decorate)([(0,r.MZ)({attribute:"aria-describedby"})],b.prototype,"ariaDescribedBy",void 0),(0,o.__decorate)([(0,r.MZ)({type:Boolean,reflect:!0})],b.prototype,"open",void 0),(0,o.__decorate)([(0,r.MZ)({reflect:!0})],b.prototype,"type",void 0),(0,o.__decorate)([(0,r.MZ)({type:String,reflect:!0,attribute:"width"})],b.prototype,"width",void 0),(0,o.__decorate)([(0,r.MZ)({type:Boolean,reflect:!0,attribute:"prevent-scrim-close"})],b.prototype,"preventScrimClose",void 0),(0,o.__decorate)([(0,r.MZ)({attribute:"header-title"})],b.prototype,"headerTitle",void 0),(0,o.__decorate)([(0,r.MZ)({attribute:"header-subtitle"})],b.prototype,"headerSubtitle",void 0),(0,o.__decorate)([(0,r.MZ)({type:String,attribute:"header-subtitle-position"})],b.prototype,"headerSubtitlePosition",void 0),(0,o.__decorate)([(0,r.MZ)({type:Boolean,reflect:!0,attribute:"flexcontent"})],b.prototype,"flexContent",void 0),(0,o.__decorate)([(0,r.wk)()],b.prototype,"_open",void 0),(0,o.__decorate)([(0,r.P)(".body")],b.prototype,"bodyContainer",void 0),(0,o.__decorate)([(0,r.wk)()],b.prototype,"_bodyScrolled",void 0),(0,o.__decorate)([(0,r.Ls)({passive:!0})],b.prototype,"_handleBodyScroll",null),b=(0,o.__decorate)([(0,r.EM)("ha-wa-dialog")],b),t()}catch(c){t(c)}})},51937:function(e,t,a){a.a(e,async function(e,o){try{a.r(t);a(23792),a(3362),a(62953);var i=a(40445),s=a(96196),r=a(77845),l=a(1087),n=a(45331),d=(a(93444),a(6),a(59646),a(18350)),h=a(77423),c=a(14503),p=a(65063),g=e([n,d]);[n,d]=g.then?(await g)():g;let u,f,v,m,w,b=e=>e;class y extends s.WF{async showDialog(e){this._params=e,this._error=void 0,this._disableNewEntities=e.entry.pref_disable_new_entities,this._disablePolling=e.entry.pref_disable_polling,this._open=!0}closeDialog(){this._open=!1}_dialogClosed(){this._error="",this._params=void 0,(0,l.r)(this,"dialog-closed",{dialog:this.localName})}render(){return this._params?(0,s.qy)(u||(u=b` <ha-wa-dialog .hass="${0}" .open="${0}" header-title="${0}" @closed="${0}"> ${0} <ha-formfield .label="${0}"> <ha-switch autofocus .checked="${0}" @change="${0}" .disabled="${0}"></ha-switch> </ha-formfield> <ha-formfield .label="${0}"> <ha-switch .checked="${0}" @change="${0}" .disabled="${0}"></ha-switch> </ha-formfield> <ha-dialog-footer slot="footer"> <ha-button appearance="plain" slot="secondaryAction" @click="${0}" .disabled="${0}"> ${0} </ha-button> <ha-button slot="primaryAction" @click="${0}" .disabled="${0}"> ${0} </ha-button> </ha-dialog-footer> </ha-wa-dialog> `),this.hass,this._open,this.hass.localize("ui.dialogs.config_entry_system_options.title",{integration:this.hass.localize(`component.${this._params.entry.domain}.title`)||this._params.entry.domain}),this._dialogClosed,this._error?(0,s.qy)(f||(f=b` <div class="error">${0}</div> `),this._error):"",(0,s.qy)(v||(v=b`<p> ${0} </p> <p class="secondary"> ${0} </p>`),this.hass.localize("ui.dialogs.config_entry_system_options.enable_new_entities_label"),this.hass.localize("ui.dialogs.config_entry_system_options.enable_new_entities_description",{integration:this.hass.localize(`component.${this._params.entry.domain}.title`)||this._params.entry.domain})),!this._disableNewEntities,this._disableNewEntitiesChanged,this._submitting,(0,s.qy)(m||(m=b`<p> ${0} </p> <p class="secondary"> ${0} </p>`),this.hass.localize("ui.dialogs.config_entry_system_options.enable_polling_label"),this.hass.localize("ui.dialogs.config_entry_system_options.enable_polling_description",{integration:this.hass.localize(`component.${this._params.entry.domain}.title`)||this._params.entry.domain})),!this._disablePolling,this._disablePollingChanged,this._submitting,this.closeDialog,this._submitting,this.hass.localize("ui.common.cancel"),this._updateEntry,this._submitting,this.hass.localize("ui.dialogs.config_entry_system_options.update")):s.s6}_disableNewEntitiesChanged(e){this._error=void 0,this._disableNewEntities=!e.target.checked}_disablePollingChanged(e){this._error=void 0,this._disablePolling=!e.target.checked}async _updateEntry(){this._submitting=!0;const e={pref_disable_new_entities:this._disableNewEntities};e.pref_disable_polling=this._disablePolling;try{(await(0,h.iH)(this.hass,this._params.entry.entry_id,e)).require_restart&&await(0,p.showAlertDialog)(this,{text:this.hass.localize("ui.dialogs.config_entry_system_options.restart_home_assistant")}),this.closeDialog()}catch(t){this._error=t.message||"Unknown error"}finally{this._submitting=!1}}static get styles(){return[c.nA,(0,s.AH)(w||(w=b`.error{color:var(--error-color)}`))]}constructor(...e){super(...e),this._submitting=!1,this._open=!1}}(0,i.__decorate)([(0,r.MZ)({attribute:!1})],y.prototype,"hass",void 0),(0,i.__decorate)([(0,r.wk)()],y.prototype,"_disableNewEntities",void 0),(0,i.__decorate)([(0,r.wk)()],y.prototype,"_disablePolling",void 0),(0,i.__decorate)([(0,r.wk)()],y.prototype,"_error",void 0),(0,i.__decorate)([(0,r.wk)()],y.prototype,"_params",void 0),(0,i.__decorate)([(0,r.wk)()],y.prototype,"_submitting",void 0),(0,i.__decorate)([(0,r.wk)()],y.prototype,"_open",void 0),y=(0,i.__decorate)([(0,r.EM)("dialog-config-entry-system-options")],y),o()}catch(u){o(u)}})},99793:function(e,t,a){var o=a(96196);let i;t.A=(0,o.AH)(i||(i=(e=>e)`:host{--width:31rem;--spacing:var(--wa-space-l);--show-duration:200ms;--hide-duration:200ms;display:none}:host([open]){display:block}.dialog{display:flex;flex-direction:column;top:0;right:0;bottom:0;left:0;width:var(--width);max-width:calc(100% - var(--wa-space-2xl));max-height:calc(100% - var(--wa-space-2xl));background-color:var(--wa-color-surface-raised);border-radius:var(--wa-panel-border-radius);border:none;box-shadow:var(--wa-shadow-l);padding:0;margin:auto}.dialog.show{animation:show-dialog var(--show-duration) ease}.dialog.show::backdrop{animation:show-backdrop var(--show-duration,200ms) ease}.dialog.hide{animation:show-dialog var(--hide-duration) ease reverse}.dialog.hide::backdrop{animation:show-backdrop var(--hide-duration,200ms) ease reverse}.dialog.pulse{animation:pulse 250ms ease}.dialog:focus{outline:0}@media screen and (max-width:420px){.dialog{max-height:80vh}}.open{display:flex;opacity:1}.header{flex:0 0 auto;display:flex;flex-wrap:nowrap;padding-inline-start:var(--spacing);padding-block-end:0;padding-inline-end:calc(var(--spacing) - var(--wa-form-control-padding-block));padding-block-start:calc(var(--spacing) - var(--wa-form-control-padding-block))}.title{align-self:center;flex:1 1 auto;font-family:inherit;font-size:var(--wa-font-size-l);font-weight:var(--wa-font-weight-heading);line-height:var(--wa-line-height-condensed);margin:0}.header-actions{align-self:start;display:flex;flex-shrink:0;flex-wrap:wrap;justify-content:end;gap:var(--wa-space-2xs);padding-inline-start:var(--spacing)}.header-actions ::slotted(wa-button),.header-actions wa-button{flex:0 0 auto;display:flex;align-items:center}.body{flex:1 1 auto;display:block;padding:var(--spacing);overflow:auto;-webkit-overflow-scrolling:touch}.body:focus{outline:0}.body:focus-visible{outline:var(--wa-focus-ring);outline-offset:var(--wa-focus-ring-offset)}.footer{flex:0 0 auto;display:flex;flex-wrap:wrap;gap:var(--wa-space-xs);justify-content:end;padding:var(--spacing);padding-block-start:0}.footer ::slotted(wa-button:not(:first-of-type)){margin-inline-start:var(--wa-spacing-xs)}.dialog::backdrop{background-color:var(--wa-color-overlay-modal,rgb(0 0 0 / .25))}@keyframes pulse{0%{scale:1}50%{scale:1.02}100%{scale:1}}@keyframes show-dialog{from{opacity:0;scale:0.8}to{opacity:1;scale:1}}@keyframes show-backdrop{from{opacity:0}to{opacity:1}}@media (forced-colors:active){.dialog{border:solid 1px #fff}}`))},93900:function(e,t,a){a.a(e,async function(e,t){try{a(23792),a(3362),a(27495),a(62953);var o=a(96196),i=a(77845),s=a(94333),r=a(32288),l=a(17051),n=a(42462),d=a(28438),h=a(98779),c=a(27259),p=a(31247),g=a(97039),u=a(92070),f=a(9395),v=a(32510),m=a(17060),w=a(88496),b=a(99793),y=e([w,m]);[w,m]=y.then?(await y)():y;let $,C,L,E=e=>e;var _=Object.defineProperty,x=Object.getOwnPropertyDescriptor,k=(e,t,a,o)=>{for(var i,s=o>1?void 0:o?x(t,a):t,r=e.length-1;r>=0;r--)(i=e[r])&&(s=(o?i(t,a,s):i(s))||s);return o&&s&&_(t,a,s),s};let M=class extends v.A{firstUpdated(){this.open&&(this.addOpenListeners(),this.dialog.showModal(),(0,g.JG)(this))}disconnectedCallback(){super.disconnectedCallback(),(0,g.I7)(this),this.removeOpenListeners()}async requestClose(e){const t=new d.L({source:e});if(this.dispatchEvent(t),t.defaultPrevented)return this.open=!0,void(0,c.Ud)(this.dialog,"pulse");this.removeOpenListeners(),await(0,c.Ud)(this.dialog,"hide"),this.open=!1,this.dialog.close(),(0,g.I7)(this);const a=this.originalTrigger;"function"==typeof(null==a?void 0:a.focus)&&setTimeout(()=>a.focus()),this.dispatchEvent(new l.Z)}addOpenListeners(){document.addEventListener("keydown",this.handleDocumentKeyDown)}removeOpenListeners(){document.removeEventListener("keydown",this.handleDocumentKeyDown)}handleDialogCancel(e){e.preventDefault(),this.dialog.classList.contains("hide")||e.target!==this.dialog||this.requestClose(this.dialog)}handleDialogClick(e){const t=e.target.closest('[data-dialog="close"]');t&&(e.stopPropagation(),this.requestClose(t))}async handleDialogPointerDown(e){e.target===this.dialog&&(this.lightDismiss?this.requestClose(this.dialog):await(0,c.Ud)(this.dialog,"pulse"))}handleOpenChange(){this.open&&!this.dialog.open?this.show():!this.open&&this.dialog.open&&(this.open=!0,this.requestClose(this.dialog))}async show(){const e=new h.k;this.dispatchEvent(e),e.defaultPrevented?this.open=!1:(this.addOpenListeners(),this.originalTrigger=document.activeElement,this.open=!0,this.dialog.showModal(),(0,g.JG)(this),requestAnimationFrame(()=>{const e=this.querySelector("[autofocus]");e&&"function"==typeof e.focus?e.focus():this.dialog.focus()}),await(0,c.Ud)(this.dialog,"show"),this.dispatchEvent(new n.q))}render(){var e;const t=!this.withoutHeader,a=this.hasSlotController.test("footer");return(0,o.qy)($||($=E` <dialog aria-labelledby="${0}" aria-describedby="${0}" part="dialog" class="${0}" @cancel="${0}" @click="${0}" @pointerdown="${0}"> ${0} <div part="body" class="body"><slot></slot></div> ${0} </dialog> `),null!==(e=this.ariaLabelledby)&&void 0!==e?e:"title",(0,r.J)(this.ariaDescribedby),(0,s.H)({dialog:!0,open:this.open}),this.handleDialogCancel,this.handleDialogClick,this.handleDialogPointerDown,t?(0,o.qy)(C||(C=E` <header part="header" class="header"> <h2 part="title" class="title" id="title"> <slot name="label"> ${0} </slot> </h2> <div part="header-actions" class="header-actions"> <slot name="header-actions"></slot> <wa-button part="close-button" exportparts="base:close-button__base" class="close" appearance="plain" @click="${0}"> <wa-icon name="xmark" label="${0}" library="system" variant="solid"></wa-icon> </wa-button> </div> </header> `),this.label.length>0?this.label:String.fromCharCode(8203),e=>this.requestClose(e.target),this.localize.term("close")):"",a?(0,o.qy)(L||(L=E` <footer part="footer" class="footer"> <slot name="footer"></slot> </footer> `)):"")}constructor(){super(...arguments),this.localize=new m.c(this),this.hasSlotController=new u.X(this,"footer","header-actions","label"),this.open=!1,this.label="",this.withoutHeader=!1,this.lightDismiss=!1,this.handleDocumentKeyDown=e=>{"Escape"===e.key&&this.open&&(e.preventDefault(),e.stopPropagation(),this.requestClose(this.dialog))}}};M.css=b.A,k([(0,i.P)(".dialog")],M.prototype,"dialog",2),k([(0,i.MZ)({type:Boolean,reflect:!0})],M.prototype,"open",2),k([(0,i.MZ)({reflect:!0})],M.prototype,"label",2),k([(0,i.MZ)({attribute:"without-header",type:Boolean,reflect:!0})],M.prototype,"withoutHeader",2),k([(0,i.MZ)({attribute:"light-dismiss",type:Boolean})],M.prototype,"lightDismiss",2),k([(0,i.MZ)({attribute:"aria-labelledby"})],M.prototype,"ariaLabelledby",2),k([(0,i.MZ)({attribute:"aria-describedby"})],M.prototype,"ariaDescribedby",2),k([(0,f.w)("open",{waitUntilFirstUpdate:!0})],M.prototype,"handleOpenChange",1),M=k([(0,i.EM)("wa-dialog")],M),document.addEventListener("click",e=>{const t=e.target.closest("[data-dialog]");if(t instanceof Element){const[e,a]=(0,p.v)(t.getAttribute("data-dialog")||"");if("open"===e&&null!=a&&a.length){const e=t.getRootNode().getElementById(a);"wa-dialog"===(null==e?void 0:e.localName)?e.open=!0:console.warn(`A dialog with an ID of "${a}" could not be found in this document.`)}}}),o.S$||document.addEventListener("pointerdown",()=>{}),t()}catch($){t($)}})},91081:function(e,t,a){function o(e,t){return{top:Math.round(e.getBoundingClientRect().top-t.getBoundingClientRect().top),left:Math.round(e.getBoundingClientRect().left-t.getBoundingClientRect().left)}}a.d(t,{A:function(){return o}})},31247:function(e,t,a){a.d(t,{v:function(){return o}});a(18111),a(22489),a(61701),a(42762);function o(e){return e.split(" ").map(e=>e.trim()).filter(e=>""!==e)}},97039:function(e,t,a){a.d(t,{I7:function(){return r},JG:function(){return s},Rt:function(){return l}});a(23792),a(27495),a(17642),a(58004),a(33853),a(45876),a(32475),a(15024),a(31698),a(25440),a(62953);var o=a(91081);const i=new Set;function s(e){if(i.add(e),!document.documentElement.classList.contains("wa-scroll-lock")){const e=function(){const e=document.documentElement.clientWidth;return Math.abs(window.innerWidth-e)}()+function(){const e=Number(getComputedStyle(document.body).paddingRight.replace(/px/,""));return isNaN(e)||!e?0:e}();let t=getComputedStyle(document.documentElement).scrollbarGutter;t&&"auto"!==t||(t="stable"),e<2&&(t=""),document.documentElement.style.setProperty("--wa-scroll-lock-gutter",t),document.documentElement.classList.add("wa-scroll-lock"),document.documentElement.style.setProperty("--wa-scroll-lock-size",`${e}px`)}}function r(e){i.delete(e),0===i.size&&(document.documentElement.classList.remove("wa-scroll-lock"),document.documentElement.style.removeProperty("--wa-scroll-lock-size"))}function l(e,t,a="vertical",i="smooth"){const s=(0,o.A)(e,t),r=s.top+t.scrollTop,l=s.left+t.scrollLeft,n=t.scrollLeft,d=t.scrollLeft+t.offsetWidth,h=t.scrollTop,c=t.scrollTop+t.offsetHeight;"horizontal"!==a&&"both"!==a||(l<n?t.scrollTo({left:l,behavior:i}):l+e.clientWidth>d&&t.scrollTo({left:l-t.offsetWidth+e.clientWidth,behavior:i})),"vertical"!==a&&"both"!==a||(r<h?t.scrollTo({top:r,behavior:i}):r+e.clientHeight>c&&t.scrollTo({top:r-t.offsetHeight+e.clientHeight,behavior:i}))}}}]);
//# sourceMappingURL=24922.6f9d9080a435ce74.js.map