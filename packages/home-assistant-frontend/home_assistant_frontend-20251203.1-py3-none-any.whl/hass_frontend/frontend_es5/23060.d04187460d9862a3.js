"use strict";(self.webpackChunkhome_assistant_frontend=self.webpackChunkhome_assistant_frontend||[]).push([["23060"],{45331:function(t,e,a){a.a(t,async function(t,e){try{a(23792),a(3362),a(62953);var o=a(40445),i=a(93900),l=a(96196),s=a(77845),n=a(32288),r=a(1087),d=a(14503),h=(a(76538),a(26300),t([i]));i=(h.then?(await h)():h)[0];let c,p,u,g,f,v,m=t=>t;const w="M19,6.41L17.59,5L12,10.59L6.41,5L5,6.41L10.59,12L5,17.59L6.41,19L12,13.41L17.59,19L19,17.59L13.41,12L19,6.41Z";class b extends l.WF{updated(t){super.updated(t),t.has("open")&&(this._open=this.open)}render(){var t,e;return(0,l.qy)(c||(c=m` <wa-dialog .open="${0}" .lightDismiss="${0}" without-header aria-labelledby="${0}" aria-describedby="${0}" @wa-show="${0}" @wa-after-show="${0}" @wa-after-hide="${0}"> <slot name="header"> <ha-dialog-header .subtitlePosition="${0}" .showBorder="${0}"> <slot name="headerNavigationIcon" slot="navigationIcon"> <ha-icon-button data-dialog="close" .label="${0}" .path="${0}"></ha-icon-button> </slot> ${0} ${0} <slot name="headerActionItems" slot="actionItems"></slot> </ha-dialog-header> </slot> <div class="body ha-scrollbar" @scroll="${0}"> <slot></slot> </div> <slot name="footer" slot="footer"></slot> </wa-dialog> `),this._open,!this.preventScrimClose,(0,n.J)(this.ariaLabelledBy||(void 0!==this.headerTitle?"ha-wa-dialog-title":void 0)),(0,n.J)(this.ariaDescribedBy),this._handleShow,this._handleAfterShow,this._handleAfterHide,this.headerSubtitlePosition,this._bodyScrolled,null!==(t=null===(e=this.hass)||void 0===e?void 0:e.localize("ui.common.close"))&&void 0!==t?t:"Close",w,void 0!==this.headerTitle?(0,l.qy)(p||(p=m`<span slot="title" class="title" id="ha-wa-dialog-title"> ${0} </span>`),this.headerTitle):(0,l.qy)(u||(u=m`<slot name="headerTitle" slot="title"></slot>`)),void 0!==this.headerSubtitle?(0,l.qy)(g||(g=m`<span slot="subtitle">${0}</span>`),this.headerSubtitle):(0,l.qy)(f||(f=m`<slot name="headerSubtitle" slot="subtitle"></slot>`)),this._handleBodyScroll)}disconnectedCallback(){super.disconnectedCallback(),this._open=!1}_handleBodyScroll(t){this._bodyScrolled=t.target.scrollTop>0}constructor(...t){super(...t),this.open=!1,this.type="standard",this.width="medium",this.preventScrimClose=!1,this.headerSubtitlePosition="below",this.flexContent=!1,this._open=!1,this._bodyScrolled=!1,this._handleShow=async()=>{this._open=!0,(0,r.r)(this,"opened"),await this.updateComplete,requestAnimationFrame(()=>{var t;null===(t=this.querySelector("[autofocus]"))||void 0===t||t.focus()})},this._handleAfterShow=()=>{(0,r.r)(this,"after-show")},this._handleAfterHide=()=>{this._open=!1,(0,r.r)(this,"closed")}}}b.styles=[d.dp,(0,l.AH)(v||(v=m`
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
    `))],(0,o.__decorate)([(0,s.MZ)({attribute:!1})],b.prototype,"hass",void 0),(0,o.__decorate)([(0,s.MZ)({attribute:"aria-labelledby"})],b.prototype,"ariaLabelledBy",void 0),(0,o.__decorate)([(0,s.MZ)({attribute:"aria-describedby"})],b.prototype,"ariaDescribedBy",void 0),(0,o.__decorate)([(0,s.MZ)({type:Boolean,reflect:!0})],b.prototype,"open",void 0),(0,o.__decorate)([(0,s.MZ)({reflect:!0})],b.prototype,"type",void 0),(0,o.__decorate)([(0,s.MZ)({type:String,reflect:!0,attribute:"width"})],b.prototype,"width",void 0),(0,o.__decorate)([(0,s.MZ)({type:Boolean,reflect:!0,attribute:"prevent-scrim-close"})],b.prototype,"preventScrimClose",void 0),(0,o.__decorate)([(0,s.MZ)({attribute:"header-title"})],b.prototype,"headerTitle",void 0),(0,o.__decorate)([(0,s.MZ)({attribute:"header-subtitle"})],b.prototype,"headerSubtitle",void 0),(0,o.__decorate)([(0,s.MZ)({type:String,attribute:"header-subtitle-position"})],b.prototype,"headerSubtitlePosition",void 0),(0,o.__decorate)([(0,s.MZ)({type:Boolean,reflect:!0,attribute:"flexcontent"})],b.prototype,"flexContent",void 0),(0,o.__decorate)([(0,s.wk)()],b.prototype,"_open",void 0),(0,o.__decorate)([(0,s.P)(".body")],b.prototype,"bodyContainer",void 0),(0,o.__decorate)([(0,s.wk)()],b.prototype,"_bodyScrolled",void 0),(0,o.__decorate)([(0,s.Ls)({passive:!0})],b.prototype,"_handleBodyScroll",null),b=(0,o.__decorate)([(0,s.EM)("ha-wa-dialog")],b),e()}catch(c){e(c)}})},35167:function(t,e,a){a.a(t,async function(t,o){try{a.r(e);a(23792),a(3362),a(62953);var i=a(40445),l=a(96196),s=a(77845),n=a(1087),r=(a(43661),a(17308),a(45331)),d=(a(2846),a(67094),a(14503)),h=t([r]);r=(h.then?(await h)():h)[0];let c,p,u=t=>t;const g="M18,11V12.5C21.19,12.5 23.09,16.05 21.33,18.71L20.24,17.62C21.06,15.96 19.85,14 18,14V15.5L15.75,13.25L18,11M18,22V20.5C14.81,20.5 12.91,16.95 14.67,14.29L15.76,15.38C14.94,17.04 16.15,19 18,19V17.5L20.25,19.75L18,22M19,3H18V1H16V3H8V1H6V3H5A2,2 0 0,0 3,5V19A2,2 0 0,0 5,21H14C13.36,20.45 12.86,19.77 12.5,19H5V8H19V10.59C19.71,10.7 20.39,10.94 21,11.31V5A2,2 0 0,0 19,3Z",f="M10,9A1,1 0 0,1 11,8A1,1 0 0,1 12,9V13.47L13.21,13.6L18.15,15.79C18.68,16.03 19,16.56 19,17.14V21.5C18.97,22.32 18.32,22.97 17.5,23H11C10.62,23 10.26,22.85 10,22.57L5.1,18.37L5.84,17.6C6.03,17.39 6.3,17.28 6.58,17.28H6.8L10,19V9M11,5A4,4 0 0,1 15,9C15,10.5 14.2,11.77 13,12.46V11.24C13.61,10.69 14,9.89 14,9A3,3 0 0,0 11,6A3,3 0 0,0 8,9C8,9.89 8.39,10.69 9,11.24V12.46C7.8,11.77 7,10.5 7,9A4,4 0 0,1 11,5Z";class v extends l.WF{showDialog(t){this._opened=!0,this._params=t}closeDialog(){return this._opened=!1,!0}_dialogClosed(){var t;null!==(t=this._params)&&void 0!==t&&t.cancel&&this._params.cancel(),this._params=void 0,(0,n.r)(this,"dialog-closed",{dialog:this.localName})}render(){return this._params?(0,l.qy)(c||(c=u` <ha-wa-dialog .hass="${0}" .open="${0}" header-title="${0}" @closed="${0}"> <ha-md-list innerRole="listbox" itemRoles="option" .innerAriaLabel="${0}" rootTabbable> <ha-md-list-item @click="${0}" type="button" .disabled="${0}"> <ha-svg-icon slot="start" .path="${0}"></ha-svg-icon> <span slot="headline"> ${0} </span> <span slot="supporting-text"> ${0} </span> <ha-icon-next slot="end"></ha-icon-next> </ha-md-list-item> <ha-md-list-item @click="${0}" type="button"> <ha-svg-icon slot="start" .path="${0}"></ha-svg-icon> <span slot="headline"> ${0} </span> <span slot="supporting-text"> ${0} </span> <ha-icon-next slot="end"></ha-icon-next> </ha-md-list-item> </ha-md-list> </ha-wa-dialog> `),this.hass,this._opened,this.hass.localize("ui.panel.config.backup.dialogs.new.title"),this._dialogClosed,this.hass.localize("ui.panel.config.backup.dialogs.new.options"),this._automatic,!this._params.config.create_backup.password,g,this.hass.localize("ui.panel.config.backup.dialogs.new.automatic.title"),this.hass.localize("ui.panel.config.backup.dialogs.new.automatic.description"),this._manual,f,this.hass.localize("ui.panel.config.backup.dialogs.new.manual.title"),this.hass.localize("ui.panel.config.backup.dialogs.new.manual.description")):l.s6}async _manual(){var t,e;null===(t=(e=this._params).submit)||void 0===t||t.call(e,"manual"),this.closeDialog()}async _automatic(){var t,e;null===(t=(e=this._params).submit)||void 0===t||t.call(e,"automatic"),this.closeDialog()}static get styles(){return[d.RF,d.nA,(0,l.AH)(p||(p=u`ha-wa-dialog{--dialog-content-padding:0}ha-md-list{background:0 0}ha-icon-next{width:24px}`))]}constructor(...t){super(...t),this._opened=!1}}(0,i.__decorate)([(0,s.MZ)({attribute:!1})],v.prototype,"hass",void 0),(0,i.__decorate)([(0,s.wk)()],v.prototype,"_opened",void 0),(0,i.__decorate)([(0,s.wk)()],v.prototype,"_params",void 0),v=(0,i.__decorate)([(0,s.EM)("ha-dialog-new-backup")],v),o()}catch(c){o(c)}})},99793:function(t,e,a){var o=a(96196);let i;e.A=(0,o.AH)(i||(i=(t=>t)`:host{--width:31rem;--spacing:var(--wa-space-l);--show-duration:200ms;--hide-duration:200ms;display:none}:host([open]){display:block}.dialog{display:flex;flex-direction:column;top:0;right:0;bottom:0;left:0;width:var(--width);max-width:calc(100% - var(--wa-space-2xl));max-height:calc(100% - var(--wa-space-2xl));background-color:var(--wa-color-surface-raised);border-radius:var(--wa-panel-border-radius);border:none;box-shadow:var(--wa-shadow-l);padding:0;margin:auto}.dialog.show{animation:show-dialog var(--show-duration) ease}.dialog.show::backdrop{animation:show-backdrop var(--show-duration,200ms) ease}.dialog.hide{animation:show-dialog var(--hide-duration) ease reverse}.dialog.hide::backdrop{animation:show-backdrop var(--hide-duration,200ms) ease reverse}.dialog.pulse{animation:pulse 250ms ease}.dialog:focus{outline:0}@media screen and (max-width:420px){.dialog{max-height:80vh}}.open{display:flex;opacity:1}.header{flex:0 0 auto;display:flex;flex-wrap:nowrap;padding-inline-start:var(--spacing);padding-block-end:0;padding-inline-end:calc(var(--spacing) - var(--wa-form-control-padding-block));padding-block-start:calc(var(--spacing) - var(--wa-form-control-padding-block))}.title{align-self:center;flex:1 1 auto;font-family:inherit;font-size:var(--wa-font-size-l);font-weight:var(--wa-font-weight-heading);line-height:var(--wa-line-height-condensed);margin:0}.header-actions{align-self:start;display:flex;flex-shrink:0;flex-wrap:wrap;justify-content:end;gap:var(--wa-space-2xs);padding-inline-start:var(--spacing)}.header-actions ::slotted(wa-button),.header-actions wa-button{flex:0 0 auto;display:flex;align-items:center}.body{flex:1 1 auto;display:block;padding:var(--spacing);overflow:auto;-webkit-overflow-scrolling:touch}.body:focus{outline:0}.body:focus-visible{outline:var(--wa-focus-ring);outline-offset:var(--wa-focus-ring-offset)}.footer{flex:0 0 auto;display:flex;flex-wrap:wrap;gap:var(--wa-space-xs);justify-content:end;padding:var(--spacing);padding-block-start:0}.footer ::slotted(wa-button:not(:first-of-type)){margin-inline-start:var(--wa-spacing-xs)}.dialog::backdrop{background-color:var(--wa-color-overlay-modal,rgb(0 0 0 / .25))}@keyframes pulse{0%{scale:1}50%{scale:1.02}100%{scale:1}}@keyframes show-dialog{from{opacity:0;scale:0.8}to{opacity:1;scale:1}}@keyframes show-backdrop{from{opacity:0}to{opacity:1}}@media (forced-colors:active){.dialog{border:solid 1px #fff}}`))},93900:function(t,e,a){a.a(t,async function(t,e){try{a(23792),a(3362),a(27495),a(62953);var o=a(96196),i=a(77845),l=a(94333),s=a(32288),n=a(17051),r=a(42462),d=a(28438),h=a(98779),c=a(27259),p=a(31247),u=a(97039),g=a(92070),f=a(9395),v=a(32510),m=a(17060),w=a(88496),b=a(99793),y=t([w,m]);[w,m]=y.then?(await y)():y;let C,L,$,M=t=>t;var _=Object.defineProperty,x=Object.getOwnPropertyDescriptor,k=(t,e,a,o)=>{for(var i,l=o>1?void 0:o?x(e,a):e,s=t.length-1;s>=0;s--)(i=t[s])&&(l=(o?i(e,a,l):i(l))||l);return o&&l&&_(e,a,l),l};let S=class extends v.A{firstUpdated(){this.open&&(this.addOpenListeners(),this.dialog.showModal(),(0,u.JG)(this))}disconnectedCallback(){super.disconnectedCallback(),(0,u.I7)(this),this.removeOpenListeners()}async requestClose(t){const e=new d.L({source:t});if(this.dispatchEvent(e),e.defaultPrevented)return this.open=!0,void(0,c.Ud)(this.dialog,"pulse");this.removeOpenListeners(),await(0,c.Ud)(this.dialog,"hide"),this.open=!1,this.dialog.close(),(0,u.I7)(this);const a=this.originalTrigger;"function"==typeof(null==a?void 0:a.focus)&&setTimeout(()=>a.focus()),this.dispatchEvent(new n.Z)}addOpenListeners(){document.addEventListener("keydown",this.handleDocumentKeyDown)}removeOpenListeners(){document.removeEventListener("keydown",this.handleDocumentKeyDown)}handleDialogCancel(t){t.preventDefault(),this.dialog.classList.contains("hide")||t.target!==this.dialog||this.requestClose(this.dialog)}handleDialogClick(t){const e=t.target.closest('[data-dialog="close"]');e&&(t.stopPropagation(),this.requestClose(e))}async handleDialogPointerDown(t){t.target===this.dialog&&(this.lightDismiss?this.requestClose(this.dialog):await(0,c.Ud)(this.dialog,"pulse"))}handleOpenChange(){this.open&&!this.dialog.open?this.show():!this.open&&this.dialog.open&&(this.open=!0,this.requestClose(this.dialog))}async show(){const t=new h.k;this.dispatchEvent(t),t.defaultPrevented?this.open=!1:(this.addOpenListeners(),this.originalTrigger=document.activeElement,this.open=!0,this.dialog.showModal(),(0,u.JG)(this),requestAnimationFrame(()=>{const t=this.querySelector("[autofocus]");t&&"function"==typeof t.focus?t.focus():this.dialog.focus()}),await(0,c.Ud)(this.dialog,"show"),this.dispatchEvent(new r.q))}render(){var t;const e=!this.withoutHeader,a=this.hasSlotController.test("footer");return(0,o.qy)(C||(C=M` <dialog aria-labelledby="${0}" aria-describedby="${0}" part="dialog" class="${0}" @cancel="${0}" @click="${0}" @pointerdown="${0}"> ${0} <div part="body" class="body"><slot></slot></div> ${0} </dialog> `),null!==(t=this.ariaLabelledby)&&void 0!==t?t:"title",(0,s.J)(this.ariaDescribedby),(0,l.H)({dialog:!0,open:this.open}),this.handleDialogCancel,this.handleDialogClick,this.handleDialogPointerDown,e?(0,o.qy)(L||(L=M` <header part="header" class="header"> <h2 part="title" class="title" id="title"> <slot name="label"> ${0} </slot> </h2> <div part="header-actions" class="header-actions"> <slot name="header-actions"></slot> <wa-button part="close-button" exportparts="base:close-button__base" class="close" appearance="plain" @click="${0}"> <wa-icon name="xmark" label="${0}" library="system" variant="solid"></wa-icon> </wa-button> </div> </header> `),this.label.length>0?this.label:String.fromCharCode(8203),t=>this.requestClose(t.target),this.localize.term("close")):"",a?(0,o.qy)($||($=M` <footer part="footer" class="footer"> <slot name="footer"></slot> </footer> `)):"")}constructor(){super(...arguments),this.localize=new m.c(this),this.hasSlotController=new g.X(this,"footer","header-actions","label"),this.open=!1,this.label="",this.withoutHeader=!1,this.lightDismiss=!1,this.handleDocumentKeyDown=t=>{"Escape"===t.key&&this.open&&(t.preventDefault(),t.stopPropagation(),this.requestClose(this.dialog))}}};S.css=b.A,k([(0,i.P)(".dialog")],S.prototype,"dialog",2),k([(0,i.MZ)({type:Boolean,reflect:!0})],S.prototype,"open",2),k([(0,i.MZ)({reflect:!0})],S.prototype,"label",2),k([(0,i.MZ)({attribute:"without-header",type:Boolean,reflect:!0})],S.prototype,"withoutHeader",2),k([(0,i.MZ)({attribute:"light-dismiss",type:Boolean})],S.prototype,"lightDismiss",2),k([(0,i.MZ)({attribute:"aria-labelledby"})],S.prototype,"ariaLabelledby",2),k([(0,i.MZ)({attribute:"aria-describedby"})],S.prototype,"ariaDescribedby",2),k([(0,f.w)("open",{waitUntilFirstUpdate:!0})],S.prototype,"handleOpenChange",1),S=k([(0,i.EM)("wa-dialog")],S),document.addEventListener("click",t=>{const e=t.target.closest("[data-dialog]");if(e instanceof Element){const[t,a]=(0,p.v)(e.getAttribute("data-dialog")||"");if("open"===t&&null!=a&&a.length){const t=e.getRootNode().getElementById(a);"wa-dialog"===(null==t?void 0:t.localName)?t.open=!0:console.warn(`A dialog with an ID of "${a}" could not be found in this document.`)}}}),o.S$||document.addEventListener("pointerdown",()=>{}),e()}catch(C){e(C)}})},91081:function(t,e,a){function o(t,e){return{top:Math.round(t.getBoundingClientRect().top-e.getBoundingClientRect().top),left:Math.round(t.getBoundingClientRect().left-e.getBoundingClientRect().left)}}a.d(e,{A:function(){return o}})},31247:function(t,e,a){a.d(e,{v:function(){return o}});a(18111),a(22489),a(61701),a(42762);function o(t){return t.split(" ").map(t=>t.trim()).filter(t=>""!==t)}},97039:function(t,e,a){a.d(e,{I7:function(){return s},JG:function(){return l},Rt:function(){return n}});a(23792),a(27495),a(17642),a(58004),a(33853),a(45876),a(32475),a(15024),a(31698),a(25440),a(62953);var o=a(91081);const i=new Set;function l(t){if(i.add(t),!document.documentElement.classList.contains("wa-scroll-lock")){const t=function(){const t=document.documentElement.clientWidth;return Math.abs(window.innerWidth-t)}()+function(){const t=Number(getComputedStyle(document.body).paddingRight.replace(/px/,""));return isNaN(t)||!t?0:t}();let e=getComputedStyle(document.documentElement).scrollbarGutter;e&&"auto"!==e||(e="stable"),t<2&&(e=""),document.documentElement.style.setProperty("--wa-scroll-lock-gutter",e),document.documentElement.classList.add("wa-scroll-lock"),document.documentElement.style.setProperty("--wa-scroll-lock-size",`${t}px`)}}function s(t){i.delete(t),0===i.size&&(document.documentElement.classList.remove("wa-scroll-lock"),document.documentElement.style.removeProperty("--wa-scroll-lock-size"))}function n(t,e,a="vertical",i="smooth"){const l=(0,o.A)(t,e),s=l.top+e.scrollTop,n=l.left+e.scrollLeft,r=e.scrollLeft,d=e.scrollLeft+e.offsetWidth,h=e.scrollTop,c=e.scrollTop+e.offsetHeight;"horizontal"!==a&&"both"!==a||(n<r?e.scrollTo({left:n,behavior:i}):n+t.clientWidth>d&&e.scrollTo({left:n-e.offsetWidth+t.clientWidth,behavior:i})),"vertical"!==a&&"both"!==a||(s<h?e.scrollTo({top:s,behavior:i}):s+t.clientHeight>c&&e.scrollTo({top:s-e.offsetHeight+t.clientHeight,behavior:i}))}}}]);
//# sourceMappingURL=23060.d04187460d9862a3.js.map