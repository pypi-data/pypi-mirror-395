/*! For license information please see 47876.729d2108416edad3.js.LICENSE.txt */
(self.webpackChunkhome_assistant_frontend=self.webpackChunkhome_assistant_frontend||[]).push([["47876"],{69709:function(t,e,i){"use strict";var n=i(59787),o=(i(74423),i(23792),i(72712),i(18111),i(22489),i(61701),i(18237),i(3362),i(27495),i(62953),i(40445)),r=i(96196),a=i(77845),l=i(1420),s=i(30015),c=i.n(s),d=i(1087),p=(i(3296),i(27208),i(48408),i(14603),i(47566),i(98721),i(2209));let u;var h=i(996);let f,m=t=>t;const g=t=>(0,r.qy)(f||(f=m`${0}`),t),v=new h.G(1e3),b={reType:(0,n.A)(/((\[!(caution|important|note|tip|warning)\])(?:\s|\\n)?)/i,{input:1,type:3}),typeToHaAlert:{caution:"error",important:"info",note:"info",tip:"success",warning:"warning"}};class x extends r.mN{disconnectedCallback(){if(super.disconnectedCallback(),this.cache){const t=this._computeCacheKey();v.set(t,this.innerHTML)}}createRenderRoot(){return this}update(t){super.update(t),void 0!==this.content&&(this._renderPromise=this._render())}async getUpdateComplete(){return await super.getUpdateComplete(),await this._renderPromise,!0}willUpdate(t){if(!this.innerHTML&&this.cache){const t=this._computeCacheKey();v.has(t)&&((0,r.XX)(g((0,l._)(v.get(t))),this.renderRoot),this._resize())}}_computeCacheKey(){return c()({content:this.content,allowSvg:this.allowSvg,allowDataUrl:this.allowDataUrl,breaks:this.breaks})}async _render(){const t=await(async(t,e,n)=>(u||(u=(0,p.LV)(new Worker(new URL(i.p+i.u("55640"),i.b)))),u.renderMarkdown(t,e,n)))(String(this.content),{breaks:this.breaks,gfm:!0},{allowSvg:this.allowSvg,allowDataUrl:this.allowDataUrl});(0,r.XX)(t.map(t=>g((0,l._)(t))),this.renderRoot),this._resize();const e=document.createTreeWalker(this,NodeFilter.SHOW_ELEMENT,null);for(;e.nextNode();){const t=e.currentNode;if(t instanceof HTMLAnchorElement&&t.host!==document.location.host)t.target="_blank",t.rel="noreferrer noopener";else if(t instanceof HTMLImageElement)this.lazyImages&&(t.loading="lazy"),t.addEventListener("load",this._resize);else if(t instanceof HTMLQuoteElement){var n;const i=(null===(n=t.firstElementChild)||void 0===n||null===(n=n.firstChild)||void 0===n?void 0:n.textContent)&&b.reType.exec(t.firstElementChild.firstChild.textContent);if(i){const{type:n}=i.groups,o=document.createElement("ha-alert");o.alertType=b.typeToHaAlert[n.toLowerCase()],o.append(...Array.from(t.childNodes).map(t=>{const e=Array.from(t.childNodes);if(!this.breaks&&e.length){var n;const t=e[0];t.nodeType===Node.TEXT_NODE&&t.textContent===i.input&&null!==(n=t.textContent)&&void 0!==n&&n.includes("\n")&&(t.textContent=t.textContent.split("\n").slice(1).join("\n"))}return e}).reduce((t,e)=>t.concat(e),[]).filter(t=>t.textContent&&t.textContent!==i.input)),e.parentNode().replaceChild(o,t)}}else t instanceof HTMLElement&&["ha-alert","ha-qr-code","ha-icon","ha-svg-icon"].includes(t.localName)&&i(96175)(`./${t.localName}`)}}constructor(...t){super(...t),this.allowSvg=!1,this.allowDataUrl=!1,this.breaks=!1,this.lazyImages=!1,this.cache=!1,this._renderPromise=Promise.resolve(),this._resize=()=>(0,d.r)(this,"content-resize")}}(0,o.__decorate)([(0,a.MZ)()],x.prototype,"content",void 0),(0,o.__decorate)([(0,a.MZ)({attribute:"allow-svg",type:Boolean})],x.prototype,"allowSvg",void 0),(0,o.__decorate)([(0,a.MZ)({attribute:"allow-data-url",type:Boolean})],x.prototype,"allowDataUrl",void 0),(0,o.__decorate)([(0,a.MZ)({type:Boolean})],x.prototype,"breaks",void 0),(0,o.__decorate)([(0,a.MZ)({type:Boolean,attribute:"lazy-images"})],x.prototype,"lazyImages",void 0),(0,o.__decorate)([(0,a.MZ)({type:Boolean})],x.prototype,"cache",void 0),x=(0,o.__decorate)([(0,a.EM)("ha-markdown-element")],x)},3587:function(t,e,i){"use strict";i(23792),i(3362),i(62953);var n=i(40445),o=i(96196),r=i(77845);i(69709);let a,l,s=t=>t;class c extends o.WF{async getUpdateComplete(){const t=await super.getUpdateComplete();return await this._markdownElement.updateComplete,t}render(){return this.content?(0,o.qy)(a||(a=s`<ha-markdown-element .content="${0}" .allowSvg="${0}" .allowDataUrl="${0}" .breaks="${0}" .lazyImages="${0}" .cache="${0}"></ha-markdown-element>`),this.content,this.allowSvg,this.allowDataUrl,this.breaks,this.lazyImages,this.cache):o.s6}constructor(...t){super(...t),this.allowSvg=!1,this.allowDataUrl=!1,this.breaks=!1,this.lazyImages=!1,this.cache=!1}}c.styles=(0,o.AH)(l||(l=s`
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
  `)),(0,n.__decorate)([(0,r.MZ)()],c.prototype,"content",void 0),(0,n.__decorate)([(0,r.MZ)({attribute:"allow-svg",type:Boolean})],c.prototype,"allowSvg",void 0),(0,n.__decorate)([(0,r.MZ)({attribute:"allow-data-url",type:Boolean})],c.prototype,"allowDataUrl",void 0),(0,n.__decorate)([(0,r.MZ)({type:Boolean})],c.prototype,"breaks",void 0),(0,n.__decorate)([(0,r.MZ)({type:Boolean,attribute:"lazy-images"})],c.prototype,"lazyImages",void 0),(0,n.__decorate)([(0,r.MZ)({type:Boolean})],c.prototype,"cache",void 0),(0,n.__decorate)([(0,r.P)("ha-markdown-element")],c.prototype,"_markdownElement",void 0),c=(0,n.__decorate)([(0,r.EM)("ha-markdown")],c)},75709:function(t,e,i){"use strict";i.d(e,{h:function(){return f}});i(23792),i(62953);var n=i(40445),o=i(68846),r=i(92347),a=i(96196),l=i(77845),s=i(63091);let c,d,p,u,h=t=>t;class f extends o.J{updated(t){super.updated(t),(t.has("invalid")||t.has("errorMessage"))&&(this.setCustomValidity(this.invalid?this.errorMessage||this.validationMessage||"Invalid":""),(this.invalid||this.validateOnInitialRender||t.has("invalid")&&void 0!==t.get("invalid"))&&this.reportValidity()),t.has("autocomplete")&&(this.autocomplete?this.formElement.setAttribute("autocomplete",this.autocomplete):this.formElement.removeAttribute("autocomplete")),t.has("autocorrect")&&(!1===this.autocorrect?this.formElement.setAttribute("autocorrect","off"):this.formElement.removeAttribute("autocorrect")),t.has("inputSpellcheck")&&(this.inputSpellcheck?this.formElement.setAttribute("spellcheck",this.inputSpellcheck):this.formElement.removeAttribute("spellcheck"))}renderIcon(t,e=!1){const i=e?"trailing":"leading";return(0,a.qy)(c||(c=h` <span class="mdc-text-field__icon mdc-text-field__icon--${0}" tabindex="${0}"> <slot name="${0}Icon"></slot> </span> `),i,e?1:-1,i)}constructor(...t){super(...t),this.icon=!1,this.iconTrailing=!1,this.autocorrect=!0}}f.styles=[r.R,(0,a.AH)(d||(d=h`.mdc-text-field__input{width:var(--ha-textfield-input-width,100%)}.mdc-text-field:not(.mdc-text-field--with-leading-icon){padding:var(--text-field-padding,0px 16px)}.mdc-text-field__affix--suffix{padding-left:var(--text-field-suffix-padding-left,12px);padding-right:var(--text-field-suffix-padding-right,0px);padding-inline-start:var(--text-field-suffix-padding-left,12px);padding-inline-end:var(--text-field-suffix-padding-right,0px);direction:ltr}.mdc-text-field--with-leading-icon{padding-inline-start:var(--text-field-suffix-padding-left,0px);padding-inline-end:var(--text-field-suffix-padding-right,16px);direction:var(--direction)}.mdc-text-field--with-leading-icon.mdc-text-field--with-trailing-icon{padding-left:var(--text-field-suffix-padding-left,0px);padding-right:var(--text-field-suffix-padding-right,0px);padding-inline-start:var(--text-field-suffix-padding-left,0px);padding-inline-end:var(--text-field-suffix-padding-right,0px)}.mdc-text-field:not(.mdc-text-field--disabled) .mdc-text-field__affix--suffix{color:var(--secondary-text-color)}.mdc-text-field:not(.mdc-text-field--disabled) .mdc-text-field__icon{color:var(--secondary-text-color)}.mdc-text-field__icon--leading{margin-inline-start:16px;margin-inline-end:8px;direction:var(--direction)}.mdc-text-field__icon--trailing{padding:var(--textfield-icon-trailing-padding,12px)}.mdc-floating-label:not(.mdc-floating-label--float-above){max-width:calc(100% - 16px)}.mdc-floating-label--float-above{max-width:calc((100% - 16px)/ .75);transition:none}input{text-align:var(--text-field-text-align,start)}input[type=color]{height:20px}::-ms-reveal{display:none}:host([no-spinner]) input::-webkit-inner-spin-button,:host([no-spinner]) input::-webkit-outer-spin-button{-webkit-appearance:none;margin:0}input[type=color]::-webkit-color-swatch-wrapper{padding:0}:host([no-spinner]) input[type=number]{-moz-appearance:textfield}.mdc-text-field__ripple{overflow:hidden}.mdc-text-field{overflow:var(--text-field-overflow)}.mdc-floating-label{padding-inline-end:16px;padding-inline-start:initial;inset-inline-start:16px!important;inset-inline-end:initial!important;transform-origin:var(--float-start);direction:var(--direction);text-align:var(--float-start);box-sizing:border-box;text-overflow:ellipsis}.mdc-text-field--with-leading-icon.mdc-text-field--filled .mdc-floating-label{max-width:calc(100% - 48px - var(--text-field-suffix-padding-left,0px));inset-inline-start:calc(48px + var(--text-field-suffix-padding-left,0px))!important;inset-inline-end:initial!important;direction:var(--direction)}.mdc-text-field__input[type=number]{direction:var(--direction)}.mdc-text-field__affix--prefix{padding-right:var(--text-field-prefix-padding-right,2px);padding-inline-end:var(--text-field-prefix-padding-right,2px);padding-inline-start:initial}.mdc-text-field:not(.mdc-text-field--disabled) .mdc-text-field__affix--prefix{color:var(--mdc-text-field-label-ink-color)}#helper-text ha-markdown{display:inline-block}`)),"rtl"===s.G.document.dir?(0,a.AH)(p||(p=h`.mdc-floating-label,.mdc-text-field--with-leading-icon,.mdc-text-field--with-leading-icon.mdc-text-field--filled .mdc-floating-label,.mdc-text-field__icon--leading,.mdc-text-field__input[type=number]{direction:rtl;--direction:rtl}`)):(0,a.AH)(u||(u=h``))],(0,n.__decorate)([(0,l.MZ)({type:Boolean})],f.prototype,"invalid",void 0),(0,n.__decorate)([(0,l.MZ)({attribute:"error-message"})],f.prototype,"errorMessage",void 0),(0,n.__decorate)([(0,l.MZ)({type:Boolean})],f.prototype,"icon",void 0),(0,n.__decorate)([(0,l.MZ)({type:Boolean})],f.prototype,"iconTrailing",void 0),(0,n.__decorate)([(0,l.MZ)()],f.prototype,"autocomplete",void 0),(0,n.__decorate)([(0,l.MZ)({type:Boolean})],f.prototype,"autocorrect",void 0),(0,n.__decorate)([(0,l.MZ)({attribute:"input-spellcheck"})],f.prototype,"inputSpellcheck",void 0),(0,n.__decorate)([(0,l.P)("input")],f.prototype,"formElement",void 0),f=(0,n.__decorate)([(0,l.EM)("ha-textfield")],f)},34439:function(t,e,i){"use strict";i.a(t,async function(t,n){try{i.r(e),i.d(e,{MoreInfoConfigurator:function(){return m}});i(89463),i(23792),i(18111),i(61701),i(62953);var o=i(40445),r=i(96196),a=i(77845),l=(i(38962),i(18350)),s=(i(3587),i(75709),t([l]));l=(s.then?(await s)():s)[0];let c,d,p,u,h,f=t=>t;class m extends r.WF{render(){var t;return"configure"!==(null===(t=this.stateObj)||void 0===t?void 0:t.state)?r.s6:(0,r.qy)(c||(c=f` <div class="container"> <ha-markdown breaks .content="${0}"></ha-markdown> ${0} ${0} ${0} </div> `),this.stateObj.attributes.description,this.stateObj.attributes.errors?(0,r.qy)(d||(d=f`<ha-alert alert-type="error"> ${0} </ha-alert>`),this.stateObj.attributes.errors):"",this.stateObj.attributes.fields.map(t=>(0,r.qy)(p||(p=f`<ha-textfield .label="${0}" .name="${0}" .type="${0}" @change="${0}"></ha-textfield>`),t.name,t.id,t.type,this._fieldChanged)),this.stateObj.attributes.submit_caption?(0,r.qy)(u||(u=f`<p class="submit"> <ha-button .disabled="${0}" @click="${0}" .loading="${0}"> ${0} </ha-button> </p>`),this._isConfiguring,this._submitClicked,this._isConfiguring,this.stateObj.attributes.submit_caption):"")}_fieldChanged(t){const e=t.target;this._fieldInput[e.name]=e.value}_submitClicked(){const t={configure_id:this.stateObj.attributes.configure_id,fields:this._fieldInput};this._isConfiguring=!0,this.hass.callService("configurator","configure",t).then(()=>{this._isConfiguring=!1},()=>{this._isConfiguring=!1})}constructor(...t){super(...t),this._isConfiguring=!1,this._fieldInput={}}}m.styles=(0,r.AH)(h||(h=f`.container{display:flex;flex-direction:column}p{margin:8px 0}a{color:var(--primary-color)}p>img{max-width:100%}p.center{text-align:center}p.submit{text-align:center;height:41px}`)),(0,o.__decorate)([(0,a.MZ)({attribute:!1})],m.prototype,"hass",void 0),(0,o.__decorate)([(0,a.MZ)({attribute:!1})],m.prototype,"stateObj",void 0),(0,o.__decorate)([(0,a.wk)()],m.prototype,"_isConfiguring",void 0),m=(0,o.__decorate)([(0,a.EM)("more-info-configurator")],m),n()}catch(c){n(c)}})},996:function(t,e,i){"use strict";i.d(e,{G:function(){return n}});i(23792),i(62953);class n{get(t){return this._cache.get(t)}set(t,e){this._cache.set(t,e),this._expiration&&window.setTimeout(()=>this._cache.delete(t),this._expiration)}has(t){return this._cache.has(t)}constructor(t){this._cache=new Map,this._expiration=t}}},96175:function(t,e,i){var n={"./ha-icon-prev":["89133","61982"],"./ha-icon-button-toolbar":["9882","26431","41983"],"./ha-alert":["38962","19695"],"./ha-icon-button-toggle":["62501","77254"],"./ha-svg-icon.ts":["67094"],"./ha-alert.ts":["38962","19695"],"./ha-icon":["88945","51146"],"./ha-icon-next.ts":["43661","63902"],"./ha-qr-code.ts":["60543","51343","62740"],"./ha-icon-overflow-menu.ts":["75248","46095","26431","22016","17521"],"./ha-icon-button-toggle.ts":["62501","77254"],"./ha-icon-button-group":["39826","13647"],"./ha-svg-icon":["67094"],"./ha-icon-button-prev":["45100","99197"],"./ha-icon-button.ts":["26300"],"./ha-icon-overflow-menu":["75248","46095","26431","22016","17521"],"./ha-icon-button-arrow-next":["99028","54101"],"./ha-icon-button-prev.ts":["45100","99197"],"./ha-icon-picker":["64138","44533","7199","46095","24876","97367","99232"],"./ha-icon-button-toolbar.ts":["9882","26431","41983"],"./ha-icon-button-arrow-prev.ts":["90248","17041"],"./ha-icon-button-next":["3059","81049"],"./ha-icon-next":["43661","63902"],"./ha-icon-picker.ts":["64138","44533","7199","46095","24876","97367","99232"],"./ha-icon-prev.ts":["89133","61982"],"./ha-icon-button-arrow-prev":["90248","17041"],"./ha-icon-button-next.ts":["3059","81049"],"./ha-icon.ts":["88945","51146"],"./ha-qr-code":["60543","51343","62740"],"./ha-icon-button":["26300"],"./ha-icon-button-group.ts":["39826","13647"],"./ha-icon-button-arrow-next.ts":["99028","54101"]};function o(t){if(!i.o(n,t))return Promise.resolve().then(function(){var e=new Error("Cannot find module '"+t+"'");throw e.code="MODULE_NOT_FOUND",e});var e=n[t],o=e[0];return Promise.all(e.slice(1).map(i.e)).then(function(){return i(o)})}o.keys=function(){return Object.keys(n)},o.id=96175,t.exports=o},13611:function(t,e,i){"use strict";var n=i(46518),o=i(22195),r=i(62106),a=i(43724),l=TypeError,s=Object.defineProperty,c=o.self!==o;try{if(a){var d=Object.getOwnPropertyDescriptor(o,"self");!c&&d&&d.get&&d.enumerable||r(o,"self",{get:function(){return o},set:function(t){if(this!==o)throw new l("Illegal invocation");s(o,"self",{value:t,writable:!0,configurable:!0,enumerable:!0})},configurable:!0,enumerable:!0})}else n({global:!0,simple:!0,forced:c},{self:o})}catch(p){}},47075:function(t,e,i){"use strict";i.d(e,{A:function(){return n}});i(89463),i(23792),i(62953);function n(t){return n="function"==typeof Symbol&&"symbol"==typeof Symbol.iterator?function(t){return typeof t}:function(t){return t&&"function"==typeof Symbol&&t.constructor===Symbol&&t!==Symbol.prototype?"symbol":typeof t},n(t)}},2209:function(t,e,i){"use strict";i.d(e,{LV:function(){return u}});i(89463),i(16280),i(23792),i(72712),i(55081),i(18111),i(61701),i(18237),i(3362),i(84864),i(57465),i(27495),i(62953);const n=Symbol("Comlink.proxy"),o=Symbol("Comlink.endpoint"),r=Symbol("Comlink.releaseProxy"),a=Symbol("Comlink.finalizer"),l=Symbol("Comlink.thrown"),s=t=>"object"==typeof t&&null!==t||"function"==typeof t,c=new Map([["proxy",{canHandle:t=>s(t)&&t[n],serialize(t){const{port1:e,port2:i}=new MessageChannel;return d(t,e),[i,[i]]},deserialize(t){return t.start(),u(t)}}],["throw",{canHandle:t=>s(t)&&l in t,serialize({value:t}){let e;return e=t instanceof Error?{isError:!0,value:{message:t.message,name:t.name,stack:t.stack}}:{isError:!1,value:t},[e,[]]},deserialize(t){if(t.isError)throw Object.assign(new Error(t.value.message),t.value);throw t.value}}]]);function d(t,e=globalThis,i=["*"]){e.addEventListener("message",function o(r){if(!r||!r.data)return;if(!function(t,e){for(const i of t){if(e===i||"*"===i)return!0;if(i instanceof RegExp&&i.test(e))return!0}return!1}(i,r.origin))return void console.warn(`Invalid origin '${r.origin}' for comlink proxy`);const{id:s,type:c,path:u}=Object.assign({path:[]},r.data),h=(r.data.argumentList||[]).map(w);let f;try{const e=u.slice(0,-1).reduce((t,e)=>t[e],t),i=u.reduce((t,e)=>t[e],t);switch(c){case"GET":f=i;break;case"SET":e[u.slice(-1)[0]]=w(r.data.value),f=!0;break;case"APPLY":f=i.apply(e,h);break;case"CONSTRUCT":f=function(t){return Object.assign(t,{[n]:!0})}(new i(...h));break;case"ENDPOINT":{const{port1:e,port2:i}=new MessageChannel;d(t,i),f=function(t,e){return x.set(t,e),t}(e,[e])}break;case"RELEASE":f=void 0;break;default:return}}catch(m){f={value:m,[l]:0}}Promise.resolve(f).catch(t=>({value:t,[l]:0})).then(i=>{const[n,r]=y(i);e.postMessage(Object.assign(Object.assign({},n),{id:s}),r),"RELEASE"===c&&(e.removeEventListener("message",o),p(e),a in t&&"function"==typeof t[a]&&t[a]())}).catch(t=>{const[i,n]=y({value:new TypeError("Unserializable return value"),[l]:0});e.postMessage(Object.assign(Object.assign({},i),{id:s}),n)})}),e.start&&e.start()}function p(t){(function(t){return"MessagePort"===t.constructor.name})(t)&&t.close()}function u(t,e){const i=new Map;return t.addEventListener("message",function(t){const{data:e}=t;if(!e||!e.id)return;const n=i.get(e.id);if(n)try{n(e)}finally{i.delete(e.id)}}),v(t,i,[],e)}function h(t){if(t)throw new Error("Proxy has been released and is not useable")}function f(t){return _(t,new Map,{type:"RELEASE"}).then(()=>{p(t)})}const m=new WeakMap,g="FinalizationRegistry"in globalThis&&new FinalizationRegistry(t=>{const e=(m.get(t)||0)-1;m.set(t,e),0===e&&f(t)});function v(t,e,i=[],n=function(){}){let a=!1;const l=new Proxy(n,{get(n,o){if(h(a),o===r)return()=>{!function(t){g&&g.unregister(t)}(l),f(t),e.clear(),a=!0};if("then"===o){if(0===i.length)return{then:()=>l};const n=_(t,e,{type:"GET",path:i.map(t=>t.toString())}).then(w);return n.then.bind(n)}return v(t,e,[...i,o])},set(n,o,r){h(a);const[l,s]=y(r);return _(t,e,{type:"SET",path:[...i,o].map(t=>t.toString()),value:l},s).then(w)},apply(n,r,l){h(a);const s=i[i.length-1];if(s===o)return _(t,e,{type:"ENDPOINT"}).then(w);if("bind"===s)return v(t,e,i.slice(0,-1));const[c,d]=b(l);return _(t,e,{type:"APPLY",path:i.map(t=>t.toString()),argumentList:c},d).then(w)},construct(n,o){h(a);const[r,l]=b(o);return _(t,e,{type:"CONSTRUCT",path:i.map(t=>t.toString()),argumentList:r},l).then(w)}});return function(t,e){const i=(m.get(e)||0)+1;m.set(e,i),g&&g.register(t,e,t)}(l,t),l}function b(t){const e=t.map(y);return[e.map(t=>t[0]),(i=e.map(t=>t[1]),Array.prototype.concat.apply([],i))];var i}const x=new WeakMap;function y(t){for(const[e,i]of c)if(i.canHandle(t)){const[n,o]=i.serialize(t);return[{type:"HANDLER",name:e,value:n},o]}return[{type:"RAW",value:t},x.get(t)||[]]}function w(t){switch(t.type){case"HANDLER":return c.get(t.name).deserialize(t.value);case"RAW":return t.value}}function _(t,e,i,n){return new Promise(o=>{const r=new Array(4).fill(0).map(()=>Math.floor(Math.random()*Number.MAX_SAFE_INTEGER).toString(16)).join("-");e.set(r,o),t.start&&t.start(),t.postMessage(Object.assign({id:r},i),n)})}}}]);
//# sourceMappingURL=47876.729d2108416edad3.js.map