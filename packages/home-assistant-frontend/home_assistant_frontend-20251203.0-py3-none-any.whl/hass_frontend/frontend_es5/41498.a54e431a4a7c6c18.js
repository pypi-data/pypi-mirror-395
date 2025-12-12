"use strict";(self.webpackChunkhome_assistant_frontend=self.webpackChunkhome_assistant_frontend||[]).push([["41498"],{77122:function(e,t,a){a.a(e,async function(e,t){try{a(74423),a(23792),a(18111),a(22489),a(61701),a(3362),a(62953);var i=a(40445),o=a(96196),r=a(77845),s=a(22786),l=a(1087),d=a(78649),n=(a(85938),a(82474)),h=e([n]);n=(h.then?(await h)():h)[0];let c,p,u,v,g,f=e=>e;const y="M21 11H3V9H21V11M21 13H3V15H21V13Z";class m extends o.WF{render(){if(!this.hass)return o.s6;const e=this._currentEntities;return(0,o.qy)(c||(c=f` ${0} <ha-sortable .disabled="${0}" handle-selector=".entity-handle" @item-moved="${0}"> <div class="list"> ${0} </div> </ha-sortable> <div> <ha-entity-picker allow-custom-entity .hass="${0}" .includeDomains="${0}" .excludeDomains="${0}" .includeEntities="${0}" .excludeEntities="${0}" .includeDeviceClasses="${0}" .includeUnitOfMeasurement="${0}" .entityFilter="${0}" .placeholder="${0}" .helper="${0}" .disabled="${0}" .createDomains="${0}" .required="${0}" @value-changed="${0}" .addButton="${0}"></ha-entity-picker> </div> `),this.label?(0,o.qy)(p||(p=f`<label>${0}</label>`),this.label):o.s6,!this.reorder||this.disabled,this._entityMoved,e.map(e=>(0,o.qy)(u||(u=f` <div class="entity"> <ha-entity-picker allow-custom-entity .curValue="${0}" .hass="${0}" .includeDomains="${0}" .excludeDomains="${0}" .includeEntities="${0}" .excludeEntities="${0}" .includeDeviceClasses="${0}" .includeUnitOfMeasurement="${0}" .entityFilter="${0}" .value="${0}" .disabled="${0}" .createDomains="${0}" @value-changed="${0}"></ha-entity-picker> ${0} </div> `),e,this.hass,this.includeDomains,this.excludeDomains,this.includeEntities,this.excludeEntities,this.includeDeviceClasses,this.includeUnitOfMeasurement,this.entityFilter,e,this.disabled,this.createDomains,this._entityChanged,this.reorder?(0,o.qy)(v||(v=f` <ha-svg-icon class="entity-handle" .path="${0}"></ha-svg-icon> `),y):o.s6)),this.hass,this.includeDomains,this.excludeDomains,this.includeEntities,this._excludeEntities(this.value,this.excludeEntities),this.includeDeviceClasses,this.includeUnitOfMeasurement,this.entityFilter,this.placeholder,this.helper,this.disabled,this.createDomains,this.required&&!e.length,this._addEntity,e.length>0)}_entityMoved(e){e.stopPropagation();const{oldIndex:t,newIndex:a}=e.detail,i=this._currentEntities,o=i[t],r=[...i];r.splice(t,1),r.splice(a,0,o),this._updateEntities(r)}get _currentEntities(){return this.value||[]}async _updateEntities(e){this.value=e,(0,l.r)(this,"value-changed",{value:e})}_entityChanged(e){e.stopPropagation();const t=e.currentTarget.curValue,a=e.detail.value;if(a===t||void 0!==a&&!(0,d.n)(a))return;const i=this._currentEntities;a&&!i.includes(a)?this._updateEntities(i.map(e=>e===t?a:e)):this._updateEntities(i.filter(e=>e!==t))}async _addEntity(e){e.stopPropagation();const t=e.detail.value;if(!t)return;if(e.currentTarget.value="",!t)return;const a=this._currentEntities;a.includes(t)||this._updateEntities([...a,t])}constructor(...e){super(...e),this.disabled=!1,this.required=!1,this.reorder=!1,this._excludeEntities=(0,s.A)((e,t)=>void 0===e?t:[...t||[],...e])}}m.styles=(0,o.AH)(g||(g=f`div{margin-top:8px}label{display:block;margin:0 0 8px}.entity{display:flex;flex-direction:row;align-items:center}.entity ha-entity-picker{flex:1}.entity-handle{padding:8px;cursor:move;cursor:grab}`)),(0,i.__decorate)([(0,r.MZ)({attribute:!1})],m.prototype,"hass",void 0),(0,i.__decorate)([(0,r.MZ)({type:Array})],m.prototype,"value",void 0),(0,i.__decorate)([(0,r.MZ)({type:Boolean})],m.prototype,"disabled",void 0),(0,i.__decorate)([(0,r.MZ)({type:Boolean})],m.prototype,"required",void 0),(0,i.__decorate)([(0,r.MZ)()],m.prototype,"label",void 0),(0,i.__decorate)([(0,r.MZ)()],m.prototype,"placeholder",void 0),(0,i.__decorate)([(0,r.MZ)()],m.prototype,"helper",void 0),(0,i.__decorate)([(0,r.MZ)({type:Array,attribute:"include-domains"})],m.prototype,"includeDomains",void 0),(0,i.__decorate)([(0,r.MZ)({type:Array,attribute:"exclude-domains"})],m.prototype,"excludeDomains",void 0),(0,i.__decorate)([(0,r.MZ)({type:Array,attribute:"include-device-classes"})],m.prototype,"includeDeviceClasses",void 0),(0,i.__decorate)([(0,r.MZ)({type:Array,attribute:"include-unit-of-measurement"})],m.prototype,"includeUnitOfMeasurement",void 0),(0,i.__decorate)([(0,r.MZ)({type:Array,attribute:"include-entities"})],m.prototype,"includeEntities",void 0),(0,i.__decorate)([(0,r.MZ)({type:Array,attribute:"exclude-entities"})],m.prototype,"excludeEntities",void 0),(0,i.__decorate)([(0,r.MZ)({attribute:!1})],m.prototype,"entityFilter",void 0),(0,i.__decorate)([(0,r.MZ)({attribute:!1,type:Array})],m.prototype,"createDomains",void 0),(0,i.__decorate)([(0,r.MZ)({type:Boolean})],m.prototype,"reorder",void 0),m=(0,i.__decorate)([(0,r.EM)("ha-entities-picker")],m),t()}catch(c){t(c)}})},93444:function(e,t,a){var i=a(40445),o=a(96196),r=a(77845);let s,l,d=e=>e;class n extends o.WF{render(){return(0,o.qy)(s||(s=d` <footer> <slot name="secondaryAction"></slot> <slot name="primaryAction"></slot> </footer> `))}static get styles(){return[(0,o.AH)(l||(l=d`footer{display:flex;gap:var(--ha-space-3);justify-content:flex-end;align-items:center;width:100%}`))]}}n=(0,i.__decorate)([(0,r.EM)("ha-dialog-footer")],n)},76538:function(e,t,a){a(23792),a(62953);var i=a(40445),o=a(96196),r=a(77845);let s,l,d,n,h,c,p=e=>e;class u extends o.WF{render(){const e=(0,o.qy)(s||(s=p`<div class="header-title"> <slot name="title"></slot> </div>`)),t=(0,o.qy)(l||(l=p`<div class="header-subtitle"> <slot name="subtitle"></slot> </div>`));return(0,o.qy)(d||(d=p` <header class="header"> <div class="header-bar"> <section class="header-navigation-icon"> <slot name="navigationIcon"></slot> </section> <section class="header-content"> ${0} </section> <section class="header-action-items"> <slot name="actionItems"></slot> </section> </div> <slot></slot> </header> `),"above"===this.subtitlePosition?(0,o.qy)(n||(n=p`${0}${0}`),t,e):(0,o.qy)(h||(h=p`${0}${0}`),e,t))}static get styles(){return[(0,o.AH)(c||(c=p`:host{display:block}:host([show-border]){border-bottom:1px solid var(--mdc-dialog-scroll-divider-color,rgba(0,0,0,.12))}.header-bar{display:flex;flex-direction:row;align-items:center;padding:0 var(--ha-space-1);box-sizing:border-box}.header-content{flex:1;padding:10px var(--ha-space-1);display:flex;flex-direction:column;justify-content:center;min-height:var(--ha-space-12);min-width:0;overflow:hidden;text-overflow:ellipsis;white-space:nowrap}.header-title{height:var(--ha-dialog-header-title-height,calc(var(--ha-font-size-xl) + var(--ha-space-1)));font-size:var(--ha-font-size-xl);line-height:var(--ha-line-height-condensed);font-weight:var(--ha-font-weight-medium);color:var(--ha-dialog-header-title-color,var(--primary-text-color))}.header-subtitle{font-size:var(--ha-font-size-m);line-height:var(--ha-line-height-normal);color:var(--ha-dialog-header-subtitle-color,var(--secondary-text-color))}@media all and (min-width:450px) and (min-height:500px){.header-bar{padding:0 var(--ha-space-2)}}.header-navigation-icon{flex:none;min-width:var(--ha-space-2);height:100%;display:flex;flex-direction:row}.header-action-items{flex:none;min-width:var(--ha-space-2);height:100%;display:flex;flex-direction:row}`))]}constructor(...e){super(...e),this.subtitlePosition="below",this.showBorder=!1}}(0,i.__decorate)([(0,r.MZ)({type:String,attribute:"subtitle-position"})],u.prototype,"subtitlePosition",void 0),(0,i.__decorate)([(0,r.MZ)({type:Boolean,reflect:!0,attribute:"show-border"})],u.prototype,"showBorder",void 0),u=(0,i.__decorate)([(0,r.EM)("ha-dialog-header")],u)},45331:function(e,t,a){a.a(e,async function(e,t){try{a(23792),a(3362),a(62953);var i=a(40445),o=a(93900),r=a(96196),s=a(77845),l=a(32288),d=a(1087),n=a(14503),h=(a(76538),a(26300),e([o]));o=(h.then?(await h)():h)[0];let c,p,u,v,g,f,y=e=>e;const m="M19,6.41L17.59,5L12,10.59L6.41,5L5,6.41L10.59,12L5,17.59L6.41,19L12,13.41L17.59,19L19,17.59L13.41,12L19,6.41Z";class _ extends r.WF{updated(e){super.updated(e),e.has("open")&&(this._open=this.open)}render(){var e,t;return(0,r.qy)(c||(c=y` <wa-dialog .open="${0}" .lightDismiss="${0}" without-header aria-labelledby="${0}" aria-describedby="${0}" @wa-show="${0}" @wa-after-show="${0}" @wa-after-hide="${0}"> <slot name="header"> <ha-dialog-header .subtitlePosition="${0}" .showBorder="${0}"> <slot name="headerNavigationIcon" slot="navigationIcon"> <ha-icon-button data-dialog="close" .label="${0}" .path="${0}"></ha-icon-button> </slot> ${0} ${0} <slot name="headerActionItems" slot="actionItems"></slot> </ha-dialog-header> </slot> <div class="body ha-scrollbar" @scroll="${0}"> <slot></slot> </div> <slot name="footer" slot="footer"></slot> </wa-dialog> `),this._open,!this.preventScrimClose,(0,l.J)(this.ariaLabelledBy||(void 0!==this.headerTitle?"ha-wa-dialog-title":void 0)),(0,l.J)(this.ariaDescribedBy),this._handleShow,this._handleAfterShow,this._handleAfterHide,this.headerSubtitlePosition,this._bodyScrolled,null!==(e=null===(t=this.hass)||void 0===t?void 0:t.localize("ui.common.close"))&&void 0!==e?e:"Close",m,void 0!==this.headerTitle?(0,r.qy)(p||(p=y`<span slot="title" class="title" id="ha-wa-dialog-title"> ${0} </span>`),this.headerTitle):(0,r.qy)(u||(u=y`<slot name="headerTitle" slot="title"></slot>`)),void 0!==this.headerSubtitle?(0,r.qy)(v||(v=y`<span slot="subtitle">${0}</span>`),this.headerSubtitle):(0,r.qy)(g||(g=y`<slot name="headerSubtitle" slot="subtitle"></slot>`)),this._handleBodyScroll)}disconnectedCallback(){super.disconnectedCallback(),this._open=!1}_handleBodyScroll(e){this._bodyScrolled=e.target.scrollTop>0}constructor(...e){super(...e),this.open=!1,this.type="standard",this.width="medium",this.preventScrimClose=!1,this.headerSubtitlePosition="below",this.flexContent=!1,this._open=!1,this._bodyScrolled=!1,this._handleShow=async()=>{this._open=!0,(0,d.r)(this,"opened"),await this.updateComplete,requestAnimationFrame(()=>{var e;null===(e=this.querySelector("[autofocus]"))||void 0===e||e.focus()})},this._handleAfterShow=()=>{(0,d.r)(this,"after-show")},this._handleAfterHide=()=>{this._open=!1,(0,d.r)(this,"closed")}}}_.styles=[n.dp,(0,r.AH)(f||(f=y`
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
    `))],(0,i.__decorate)([(0,s.MZ)({attribute:!1})],_.prototype,"hass",void 0),(0,i.__decorate)([(0,s.MZ)({attribute:"aria-labelledby"})],_.prototype,"ariaLabelledBy",void 0),(0,i.__decorate)([(0,s.MZ)({attribute:"aria-describedby"})],_.prototype,"ariaDescribedBy",void 0),(0,i.__decorate)([(0,s.MZ)({type:Boolean,reflect:!0})],_.prototype,"open",void 0),(0,i.__decorate)([(0,s.MZ)({reflect:!0})],_.prototype,"type",void 0),(0,i.__decorate)([(0,s.MZ)({type:String,reflect:!0,attribute:"width"})],_.prototype,"width",void 0),(0,i.__decorate)([(0,s.MZ)({type:Boolean,reflect:!0,attribute:"prevent-scrim-close"})],_.prototype,"preventScrimClose",void 0),(0,i.__decorate)([(0,s.MZ)({attribute:"header-title"})],_.prototype,"headerTitle",void 0),(0,i.__decorate)([(0,s.MZ)({attribute:"header-subtitle"})],_.prototype,"headerSubtitle",void 0),(0,i.__decorate)([(0,s.MZ)({type:String,attribute:"header-subtitle-position"})],_.prototype,"headerSubtitlePosition",void 0),(0,i.__decorate)([(0,s.MZ)({type:Boolean,reflect:!0,attribute:"flexcontent"})],_.prototype,"flexContent",void 0),(0,i.__decorate)([(0,s.wk)()],_.prototype,"_open",void 0),(0,i.__decorate)([(0,s.P)(".body")],_.prototype,"bodyContainer",void 0),(0,i.__decorate)([(0,s.wk)()],_.prototype,"_bodyScrolled",void 0),(0,i.__decorate)([(0,s.Ls)({passive:!0})],_.prototype,"_handleBodyScroll",null),_=(0,i.__decorate)([(0,s.EM)("ha-wa-dialog")],_),t()}catch(c){t(c)}})},284:function(e,t,a){a.a(e,async function(e,i){try{a.r(t),a.d(t,{DialogEditHome:function(){return y}});a(23792),a(3362),a(62953);var o=a(40445),r=a(96196),s=a(77845),l=a(1087),d=a(77122),n=(a(38962),a(18350)),h=(a(93444),a(45331)),c=a(14503),p=e([d,n,h]);[d,n,h]=p.then?(await p)():p;let u,v,g,f=e=>e;class y extends r.WF{showDialog(e){this._params=e,this._config=Object.assign({},e.config),this._open=!0}closeDialog(){return this._open=!1,!0}_dialogClosed(){this._params=void 0,this._config=void 0,this._submitting=!1,(0,l.r)(this,"dialog-closed",{dialog:this.localName})}render(){var e;return this._params?(0,r.qy)(u||(u=f` <ha-wa-dialog .hass="${0}" .open="${0}" .headerTitle="${0}" @closed="${0}"> <p class="description"> ${0} </p> <ha-entities-picker autofocus .hass="${0}" .value="${0}" .label="${0}" .placeholder="${0}" .helper="${0}" reorder allow-custom-entity @value-changed="${0}"></ha-entities-picker> <ha-alert alert-type="info"> ${0} </ha-alert> <ha-dialog-footer slot="footer"> <ha-button appearance="plain" slot="secondaryAction" @click="${0}" .disabled="${0}"> ${0} </ha-button> <ha-button slot="primaryAction" @click="${0}" .disabled="${0}"> ${0} </ha-button> </ha-dialog-footer> </ha-wa-dialog> `),this.hass,this._open,this.hass.localize("ui.panel.home.editor.title"),this._dialogClosed,this.hass.localize("ui.panel.home.editor.description"),this.hass,(null===(e=this._config)||void 0===e?void 0:e.favorite_entities)||[],this.hass.localize("ui.panel.lovelace.editor.strategy.home.favorite_entities"),this.hass.localize("ui.panel.lovelace.editor.strategy.home.add_favorite_entity"),this.hass.localize("ui.panel.home.editor.favorite_entities_helper"),this._favoriteEntitiesChanged,this.hass.localize("ui.panel.home.editor.areas_hint",{areas_page:(0,r.qy)(v||(v=f`<a href="/config/areas?historyBack=1" @click="${0}">${0}</a>`),this.closeDialog,this.hass.localize("ui.panel.home.editor.areas_page"))}),this.closeDialog,this._submitting,this.hass.localize("ui.common.cancel"),this._save,this._submitting,this.hass.localize("ui.common.save")):r.s6}_favoriteEntitiesChanged(e){const t=e.detail.value;this._config=Object.assign(Object.assign({},this._config),{},{favorite_entities:t.length>0?t:void 0})}async _save(){if(this._params&&this._config){this._submitting=!0;try{await this._params.saveConfig(this._config),this.closeDialog()}catch(e){console.error("Failed to save home configuration:",e)}finally{this._submitting=!1}}}constructor(...e){super(...e),this._open=!1,this._submitting=!1}}y.styles=[c.nA,(0,r.AH)(g||(g=f`ha-wa-dialog{--dialog-content-padding:var(--ha-space-6)}.description{margin:0 0 var(--ha-space-4) 0;color:var(--secondary-text-color)}ha-entities-picker{display:block}ha-alert{display:block;margin-top:var(--ha-space-4)}`))],(0,o.__decorate)([(0,s.MZ)({attribute:!1})],y.prototype,"hass",void 0),(0,o.__decorate)([(0,s.wk)()],y.prototype,"_params",void 0),(0,o.__decorate)([(0,s.wk)()],y.prototype,"_config",void 0),(0,o.__decorate)([(0,s.wk)()],y.prototype,"_open",void 0),(0,o.__decorate)([(0,s.wk)()],y.prototype,"_submitting",void 0),y=(0,o.__decorate)([(0,s.EM)("dialog-edit-home")],y),i()}catch(u){i(u)}})},85614:function(e,t,a){a.d(t,{i:function(){return i}});a(23792),a(3362),a(62953);const i=async()=>{await Promise.all([a.e("38085"),a.e("1506")]).then(a.bind(a,40772))}}}]);
//# sourceMappingURL=41498.a54e431a4a7c6c18.js.map