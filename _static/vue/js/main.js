(function(e){function t(t){for(var o,s,i=t[0],l=t[1],c=t[2],d=0,f=[];d<i.length;d++)s=i[d],Object.prototype.hasOwnProperty.call(r,s)&&r[s]&&f.push(r[s][0]),r[s]=0;for(o in l)Object.prototype.hasOwnProperty.call(l,o)&&(e[o]=l[o]);u&&u(t);while(f.length)f.shift()();return a.push.apply(a,c||[]),n()}function n(){for(var e,t=0;t<a.length;t++){for(var n=a[t],o=!0,i=1;i<n.length;i++){var l=n[i];0!==r[l]&&(o=!1)}o&&(a.splice(t--,1),e=s(s.s=n[0]))}return e}var o={},r={main:0},a=[];function s(t){if(o[t])return o[t].exports;var n=o[t]={i:t,l:!1,exports:{}};return e[t].call(n.exports,n,n.exports,s),n.l=!0,n.exports}s.m=e,s.c=o,s.d=function(e,t,n){s.o(e,t)||Object.defineProperty(e,t,{enumerable:!0,get:n})},s.r=function(e){"undefined"!==typeof Symbol&&Symbol.toStringTag&&Object.defineProperty(e,Symbol.toStringTag,{value:"Module"}),Object.defineProperty(e,"__esModule",{value:!0})},s.t=function(e,t){if(1&t&&(e=s(e)),8&t)return e;if(4&t&&"object"===typeof e&&e&&e.__esModule)return e;var n=Object.create(null);if(s.r(n),Object.defineProperty(n,"default",{enumerable:!0,value:e}),2&t&&"string"!=typeof e)for(var o in e)s.d(n,o,function(t){return e[t]}.bind(null,o));return n},s.n=function(e){var t=e&&e.__esModule?function(){return e["default"]}:function(){return e};return s.d(t,"a",t),t},s.o=function(e,t){return Object.prototype.hasOwnProperty.call(e,t)},s.p="/static/vue/";var i=window["webpackJsonp"]=window["webpackJsonp"]||[],l=i.push.bind(i);i.push=t,i=i.slice();for(var c=0;c<i.length;c++)t(i[c]);var u=l;a.push([0,"chunk-vendors"]),n()})({0:function(e,t,n){e.exports=n("56d7")},"034f":function(e,t,n){"use strict";var o=n("85ec"),r=n.n(o);r.a},"56d7":function(e,t,n){"use strict";n.r(t);n("e260"),n("e6cf"),n("cca6"),n("a79d");var o=n("a026"),r=function(){var e=this,t=e.$createElement,n=e._self._c||t;return n("v-app",{staticClass:"main-app"},[n("v-row",{attrs:{align:"center",justify:"center"}},[n("div",{},[!e.no_q_left&&e.body?n("v-card",{staticClass:"py-12 main_card",attrs:{flat:""}},[n("v-card-text",[n("v-row",{attrs:{align:"center",justify:"center"}},[n("v-col",{attrs:{cols:"12"}},[e.lead?n("h4",{style:{color:"black"}},[e._v(e._s(e.lead))]):e._e()]),n("v-col",{attrs:{cols:"12"}},[n("v-card-title",{staticClass:"justify-center text-center",style:{background:e.fieldCol,"border-radius":"25px"}},[n("transition",{attrs:{name:"custom-classes-transition","enter-active-class":"animate__animated animate__bounceIn",appear:""}},[n("div",{key:e.body,staticClass:"white--text text-center"},[n("span",{staticClass:"bodytext"},[e._v(" "+e._s(e.body)+" ")])])])],1)],1),n("v-col",{attrs:{cols:"12"}},[e.no_q_left?n("div",[e._v("No questions left")]):e._e()]),n("v-col",{attrs:{cols:"12"}},[n("v-btn-toggle",{model:{value:e.value,callback:function(t){e.value=t},expression:"value"}},e._l(e.likert,(function(t){return n("v-btn",{key:t,on:{click:function(n){return e.answer(t)}}},[e._v(" "+e._s(t)+" ")])})),1)],1)],1)],1)],1):e._e()],1)])],1)},a=[],s={data:function(){return{lead:window.field_desc["lead"],trans:!0,no_q_left:!1,body:"",qid:null,field:null,value:null,toggle_exclusive:void 0,likert:this._.range(0,11),progressValue:0}},computed:{fieldCol:function(){var e={attitude:"black",average_attitude:"red",friend:"blue",absolute_importance:"darkgrey"};return e[this.field]||"black"}},watch:{progressValue:function(e){window.vueProgress.progressValue=e},no_q_left:function(e){e&&document.getElementById("form").submit()}},mounted:function(){var e=this;this.$options.sockets.onmessage=function(t){var n=JSON.parse(t["data"]);e.trans=!1,e.no_q_left=n.no_q_left,e.body=n.body,e.qid=n.id,e.field=n.field,e.value=n.value,e.progressValue=n.progress_value},this.trans=!0,this.$options.sockets.onopen=function(t){e.$socket.sendObj({info_request:!0})}},methods:{answer:function(e){this.trans=!0,this.$socket.sendObj({answer:!0,qid:this.qid,field:this.field,value:e}),this.value=null}}},i=s,l=(n("034f"),n("2877")),c=n("6544"),u=n.n(c),d=n("7496"),f=n("8336"),p=n("a609"),v=n("b0af"),b=n("99d9"),_=n("62ad"),h=n("0fd9"),y=Object(l["a"])(i,r,a,!1,null,null,null),w=y.exports;u()(y,{VApp:d["a"],VBtn:f["a"],VBtnToggle:p["a"],VCard:v["a"],VCardText:b["b"],VCardTitle:b["c"],VCol:_["a"],VRow:h["a"]});var g=n("b408"),m=n.n(g),k=(n("d1e78"),n("5363"),n("ce5b")),j=n.n(k),x=(n("bf40"),n("9955")),O=n.n(x),q=n("2ef0"),V=n.n(q);o["default"].use(O.a,{name:"custom",lodash:V.a}),o["default"].use(j.a),o["default"].config.productionTip=!1;var C="https:"===window.location.protocol?"wss":"ws",P=C+"://"+window.location.host+window.socket_path;o["default"].use(m.a,P,{format:"json",reconnection:!0,reconnectionAttempts:5,reconnectionDelay:3e3}),window.vueOpinion=new o["default"]({vuetify:new j.a({defaultAssets:{font:!0,icons:"mdi"},icons:{iconfont:"mdi"}}),render:function(e){return e(w)}}).$mount("#app")},"85ec":function(e,t,n){}});