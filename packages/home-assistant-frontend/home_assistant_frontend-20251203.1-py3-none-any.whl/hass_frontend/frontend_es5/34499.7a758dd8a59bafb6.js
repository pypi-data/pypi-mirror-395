"use strict";(self.webpackChunkhome_assistant_frontend=self.webpackChunkhome_assistant_frontend||[]).push([["34499"],{69093:function(e,t,a){a.d(t,{t:function(){return o}});var i=a(71727);const o=e=>(0,i.m)(e.entity_id)},82286:function(e,t,a){a.d(t,{$:function(){return i}});const i=(e,t)=>o(e.attributes,t),o=(e,t)=>0!==(e.supported_features&t)},38962:function(e,t,a){a.r(t);a(23792),a(62953);var i=a(40445),o=a(96196),r=a(77845),s=a(94333),l=a(1087);a(26300),a(67094);let n,d,h,c,p=e=>e;const u={info:"M11,9H13V7H11M12,20C7.59,20 4,16.41 4,12C4,7.59 7.59,4 12,4C16.41,4 20,7.59 20,12C20,16.41 16.41,20 12,20M12,2A10,10 0 0,0 2,12A10,10 0 0,0 12,22A10,10 0 0,0 22,12A10,10 0 0,0 12,2M11,17H13V11H11V17Z",warning:"M12,2L1,21H23M12,6L19.53,19H4.47M11,10V14H13V10M11,16V18H13V16",error:"M11,15H13V17H11V15M11,7H13V13H11V7M12,2C6.47,2 2,6.5 2,12A10,10 0 0,0 12,22A10,10 0 0,0 22,12A10,10 0 0,0 12,2M12,20A8,8 0 0,1 4,12A8,8 0 0,1 12,4A8,8 0 0,1 20,12A8,8 0 0,1 12,20Z",success:"M20,12A8,8 0 0,1 12,20A8,8 0 0,1 4,12A8,8 0 0,1 12,4C12.76,4 13.5,4.11 14.2,4.31L15.77,2.74C14.61,2.26 13.34,2 12,2A10,10 0 0,0 2,12A10,10 0 0,0 12,22A10,10 0 0,0 22,12M7.91,10.08L6.5,11.5L11,16L21,6L19.59,4.58L11,13.17L7.91,10.08Z"};class v extends o.WF{render(){return(0,o.qy)(n||(n=p` <div class="issue-type ${0}" role="alert"> <div class="icon ${0}"> <slot name="icon"> <ha-svg-icon .path="${0}"></ha-svg-icon> </slot> </div> <div class="${0}"> <div class="main-content"> ${0} <slot></slot> </div> <div class="action"> <slot name="action"> ${0} </slot> </div> </div> </div> `),(0,s.H)({[this.alertType]:!0}),this.title?"":"no-title",u[this.alertType],(0,s.H)({content:!0,narrow:this.narrow}),this.title?(0,o.qy)(d||(d=p`<div class="title">${0}</div>`),this.title):o.s6,this.dismissable?(0,o.qy)(h||(h=p`<ha-icon-button @click="${0}" label="Dismiss alert" .path="${0}"></ha-icon-button>`),this._dismissClicked,"M19,6.41L17.59,5L12,10.59L6.41,5L5,6.41L10.59,12L5,17.59L6.41,19L12,13.41L17.59,19L19,17.59L13.41,12L19,6.41Z"):o.s6)}_dismissClicked(){(0,l.r)(this,"alert-dismissed-clicked")}constructor(...e){super(...e),this.title="",this.alertType="info",this.dismissable=!1,this.narrow=!1}}v.styles=(0,o.AH)(c||(c=p`.issue-type{position:relative;padding:8px;display:flex}.icon{height:var(--ha-alert-icon-size,24px);width:var(--ha-alert-icon-size,24px)}.issue-type::after{position:absolute;top:0;right:0;bottom:0;left:0;opacity:.12;pointer-events:none;content:"";border-radius:var(--ha-border-radius-sm)}.icon.no-title{align-self:center}.content{display:flex;justify-content:space-between;align-items:center;width:100%;text-align:var(--float-start)}.content.narrow{flex-direction:column;align-items:flex-end}.action{z-index:1;width:min-content;--mdc-theme-primary:var(--primary-text-color)}.main-content{overflow-wrap:anywhere;word-break:break-word;line-height:normal;margin-left:8px;margin-right:0;margin-inline-start:8px;margin-inline-end:8px}.title{margin-top:2px;font-weight:var(--ha-font-weight-bold)}.action ha-icon-button{--mdc-theme-primary:var(--primary-text-color);--mdc-icon-button-size:36px}.issue-type.info>.icon{color:var(--info-color)}.issue-type.info::after{background-color:var(--info-color)}.issue-type.warning>.icon{color:var(--warning-color)}.issue-type.warning::after{background-color:var(--warning-color)}.issue-type.error>.icon{color:var(--error-color)}.issue-type.error::after{background-color:var(--error-color)}.issue-type.success>.icon{color:var(--success-color)}.issue-type.success::after{background-color:var(--success-color)}:host ::slotted(ul){margin:0;padding-inline-start:20px}`)),(0,i.__decorate)([(0,r.MZ)()],v.prototype,"title",void 0),(0,i.__decorate)([(0,r.MZ)({attribute:"alert-type"})],v.prototype,"alertType",void 0),(0,i.__decorate)([(0,r.MZ)({type:Boolean})],v.prototype,"dismissable",void 0),(0,i.__decorate)([(0,r.MZ)({type:Boolean})],v.prototype,"narrow",void 0),v=(0,i.__decorate)([(0,r.EM)("ha-alert")],v)},93444:function(e,t,a){var i=a(40445),o=a(96196),r=a(77845);let s,l,n=e=>e;class d extends o.WF{render(){return(0,o.qy)(s||(s=n` <footer> <slot name="secondaryAction"></slot> <slot name="primaryAction"></slot> </footer> `))}static get styles(){return[(0,o.AH)(l||(l=n`footer{display:flex;gap:var(--ha-space-3);justify-content:flex-end;align-items:center;width:100%}`))]}}d=(0,i.__decorate)([(0,r.EM)("ha-dialog-footer")],d)},45331:function(e,t,a){a.a(e,async function(e,t){try{a(23792),a(3362),a(62953);var i=a(40445),o=a(93900),r=a(96196),s=a(77845),l=a(32288),n=a(1087),d=a(14503),h=(a(76538),a(26300),e([o]));o=(h.then?(await h)():h)[0];let c,p,u,v,g,f,m=e=>e;const _="M19,6.41L17.59,5L12,10.59L6.41,5L5,6.41L10.59,12L5,17.59L6.41,19L12,13.41L17.59,19L19,17.59L13.41,12L19,6.41Z";class y extends r.WF{updated(e){super.updated(e),e.has("open")&&(this._open=this.open)}render(){var e,t;return(0,r.qy)(c||(c=m` <wa-dialog .open="${0}" .lightDismiss="${0}" without-header aria-labelledby="${0}" aria-describedby="${0}" @wa-show="${0}" @wa-after-show="${0}" @wa-after-hide="${0}"> <slot name="header"> <ha-dialog-header .subtitlePosition="${0}" .showBorder="${0}"> <slot name="headerNavigationIcon" slot="navigationIcon"> <ha-icon-button data-dialog="close" .label="${0}" .path="${0}"></ha-icon-button> </slot> ${0} ${0} <slot name="headerActionItems" slot="actionItems"></slot> </ha-dialog-header> </slot> <div class="body ha-scrollbar" @scroll="${0}"> <slot></slot> </div> <slot name="footer" slot="footer"></slot> </wa-dialog> `),this._open,!this.preventScrimClose,(0,l.J)(this.ariaLabelledBy||(void 0!==this.headerTitle?"ha-wa-dialog-title":void 0)),(0,l.J)(this.ariaDescribedBy),this._handleShow,this._handleAfterShow,this._handleAfterHide,this.headerSubtitlePosition,this._bodyScrolled,null!==(e=null===(t=this.hass)||void 0===t?void 0:t.localize("ui.common.close"))&&void 0!==e?e:"Close",_,void 0!==this.headerTitle?(0,r.qy)(p||(p=m`<span slot="title" class="title" id="ha-wa-dialog-title"> ${0} </span>`),this.headerTitle):(0,r.qy)(u||(u=m`<slot name="headerTitle" slot="title"></slot>`)),void 0!==this.headerSubtitle?(0,r.qy)(v||(v=m`<span slot="subtitle">${0}</span>`),this.headerSubtitle):(0,r.qy)(g||(g=m`<slot name="headerSubtitle" slot="subtitle"></slot>`)),this._handleBodyScroll)}disconnectedCallback(){super.disconnectedCallback(),this._open=!1}_handleBodyScroll(e){this._bodyScrolled=e.target.scrollTop>0}constructor(...e){super(...e),this.open=!1,this.type="standard",this.width="medium",this.preventScrimClose=!1,this.headerSubtitlePosition="below",this.flexContent=!1,this._open=!1,this._bodyScrolled=!1,this._handleShow=async()=>{this._open=!0,(0,n.r)(this,"opened"),await this.updateComplete,requestAnimationFrame(()=>{var e;null===(e=this.querySelector("[autofocus]"))||void 0===e||e.focus()})},this._handleAfterShow=()=>{(0,n.r)(this,"after-show")},this._handleAfterHide=()=>{this._open=!1,(0,n.r)(this,"closed")}}}y.styles=[d.dp,(0,r.AH)(f||(f=m`
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
    `))],(0,i.__decorate)([(0,s.MZ)({attribute:!1})],y.prototype,"hass",void 0),(0,i.__decorate)([(0,s.MZ)({attribute:"aria-labelledby"})],y.prototype,"ariaLabelledBy",void 0),(0,i.__decorate)([(0,s.MZ)({attribute:"aria-describedby"})],y.prototype,"ariaDescribedBy",void 0),(0,i.__decorate)([(0,s.MZ)({type:Boolean,reflect:!0})],y.prototype,"open",void 0),(0,i.__decorate)([(0,s.MZ)({reflect:!0})],y.prototype,"type",void 0),(0,i.__decorate)([(0,s.MZ)({type:String,reflect:!0,attribute:"width"})],y.prototype,"width",void 0),(0,i.__decorate)([(0,s.MZ)({type:Boolean,reflect:!0,attribute:"prevent-scrim-close"})],y.prototype,"preventScrimClose",void 0),(0,i.__decorate)([(0,s.MZ)({attribute:"header-title"})],y.prototype,"headerTitle",void 0),(0,i.__decorate)([(0,s.MZ)({attribute:"header-subtitle"})],y.prototype,"headerSubtitle",void 0),(0,i.__decorate)([(0,s.MZ)({type:String,attribute:"header-subtitle-position"})],y.prototype,"headerSubtitlePosition",void 0),(0,i.__decorate)([(0,s.MZ)({type:Boolean,reflect:!0,attribute:"flexcontent"})],y.prototype,"flexContent",void 0),(0,i.__decorate)([(0,s.wk)()],y.prototype,"_open",void 0),(0,i.__decorate)([(0,s.P)(".body")],y.prototype,"bodyContainer",void 0),(0,i.__decorate)([(0,s.wk)()],y.prototype,"_bodyScrolled",void 0),(0,i.__decorate)([(0,s.Ls)({passive:!0})],y.prototype,"_handleBodyScroll",null),y=(0,i.__decorate)([(0,s.EM)("ha-wa-dialog")],y),t()}catch(c){t(c)}})},24367:function(e,t,a){a.d(t,{L:function(){return o},z:function(){return r}});var i=a(23832);const o=["input_boolean","input_button","input_text","input_number","input_datetime","input_select","counter","timer","schedule"],r=(0,i.g)(o)},84309:function(e,t,a){a.a(e,async function(e,i){try{a.r(t),a.d(t,{DialogLovelaceResourceDetail:function(){return g}});a(23792),a(3362),a(42762),a(62953);var o=a(40445),r=a(96196),s=a(77845),l=a(22786),n=a(1087),d=a(45331),h=(a(93444),a(38962),a(52763),a(18350)),c=e([d,h]);[d,h]=c.then?(await c)():c;let p,u=e=>e;const v=e=>{if(!e)return;const t=e.split(".").pop()||"";return"css"===t?"css":"js"===t?"module":void 0};class g extends r.WF{showDialog(e){this._params=e,this._error=void 0,this._params.resource?this._data={url:this._params.resource.url,res_type:this._params.resource.type}:this._data={url:""},this._open=!0}closeDialog(){this._open=!1}_dialogClosed(){this._params=void 0,(0,n.r)(this,"dialog-closed",{dialog:this.localName})}render(){var e,t,a;if(!this._params)return r.s6;const i=!(null!==(e=this._data)&&void 0!==e&&e.url)||""===this._data.url.trim(),o=(null===(t=this._params.resource)||void 0===t?void 0:t.url)||this.hass.localize("ui.panel.config.lovelace.resources.detail.new_resource");return(0,r.qy)(p||(p=u` <ha-wa-dialog .hass="${0}" .open="${0}" prevent-scrim-close header-title="${0}" @closed="${0}"> <ha-alert alert-type="warning" .title="${0}"> ${0} </ha-alert> <ha-form autofocus .schema="${0}" .data="${0}" .hass="${0}" .error="${0}" .computeLabel="${0}" @value-changed="${0}"></ha-form> <ha-dialog-footer slot="footer"> <ha-button appearance="plain" slot="secondaryAction" @click="${0}"> ${0} </ha-button> <ha-button slot="primaryAction" @click="${0}" .disabled="${0}"> ${0} </ha-button> </ha-dialog-footer> </ha-wa-dialog> `),this.hass,this._open,o,this._dialogClosed,this.hass.localize("ui.panel.config.lovelace.resources.detail.warning_header"),this.hass.localize("ui.panel.config.lovelace.resources.detail.warning_text"),this._schema(this._data),this._data,this.hass,this._error,this._computeLabel,this._valueChanged,this.closeDialog,this.hass.localize("ui.common.cancel"),this._updateResource,i||!(null!==(a=this._data)&&void 0!==a&&a.res_type)||this._submitting,this._params.resource?this.hass.localize("ui.panel.config.lovelace.resources.detail.update"):this.hass.localize("ui.panel.config.lovelace.resources.detail.create"))}_valueChanged(e){if(this._data=e.detail.value,!this._data.res_type){const e=v(this._data.url);if(!e)return;this._data=Object.assign(Object.assign({},this._data),{},{res_type:e})}}async _updateResource(){var e;if(null!==(e=this._data)&&void 0!==e&&e.res_type){this._submitting=!0;try{this._params.resource?await this._params.updateResource(this._data):await this._params.createResource(this._data),this._params=void 0}catch(t){this._error={base:(null==t?void 0:t.message)||"Unknown error"}}finally{this._submitting=!1}}}constructor(...e){super(...e),this._submitting=!1,this._open=!1,this._schema=(0,l.A)(e=>[{name:"url",required:!0,selector:{text:{}}},{name:"res_type",required:!0,selector:{select:{options:[{value:"module",label:this.hass.localize("ui.panel.config.lovelace.resources.types.module")},{value:"css",label:this.hass.localize("ui.panel.config.lovelace.resources.types.css")},..."js"===e.type?[{value:"js",label:this.hass.localize("ui.panel.config.lovelace.resources.types.js")}]:[],..."html"===e.type?[{value:"html",label:this.hass.localize("ui.panel.config.lovelace.resources.types.html")}]:[]]}}}]),this._computeLabel=e=>this.hass.localize(`ui.panel.config.lovelace.resources.detail.${"res_type"===e.name?"type":e.name}`)}}(0,o.__decorate)([(0,s.MZ)({attribute:!1})],g.prototype,"hass",void 0),(0,o.__decorate)([(0,s.wk)()],g.prototype,"_params",void 0),(0,o.__decorate)([(0,s.wk)()],g.prototype,"_data",void 0),(0,o.__decorate)([(0,s.wk)()],g.prototype,"_error",void 0),(0,o.__decorate)([(0,s.wk)()],g.prototype,"_submitting",void 0),(0,o.__decorate)([(0,s.wk)()],g.prototype,"_open",void 0),g=(0,o.__decorate)([(0,s.EM)("dialog-lovelace-resource-detail")],g),i()}catch(p){i(p)}})}}]);
//# sourceMappingURL=34499.7a758dd8a59bafb6.js.map