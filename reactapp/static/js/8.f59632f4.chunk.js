(window.webpackJsonp=window.webpackJsonp||[]).push([[8],{175:function(e,a,t){"use strict";t.d(a,"a",function(){return l});var n=t(0),c=t.n(n),r=t(2),l=function(e){var a=e.text,t=e.icon,l=e.active,i=e.handleShowActiveMenu,s=Object(n.useCallback)(function(){i&&i(a)},[a]);return c.a.createElement("button",{onClick:s,className:"button-icon ".concat(l?"active":"")}," ",t&&c.a.createElement(r.a,{src:t})," ",a," ")}},176:function(e,a,t){"use strict";t.d(a,"a",function(){return i});var n=t(0),c=t.n(n),r=t(3),l=t(65),i=function(e){var a=e.img,t=e.title,n=e.desc,i=e.value,s=e.rating,o=e.slug;return c.a.createElement(r.b,{to:"/activities-link/".concat(o),style:{textDecoration:"none"}},c.a.createElement("div",{className:"top-attractions-wrapper-card"},c.a.createElement("div",{className:"top-attractions-card"},c.a.createElement("span",null,i),c.a.createElement("img",{src:a,alt:"top attr"}),c.a.createElement("div",{className:"content-text"},c.a.createElement("h2",null,t),c.a.createElement("div",null,[0,1,2,3,4].map(function(e){return c.a.createElement(l.a,{key:e,value:100*(s-e),color:"#FFCB45"})})),c.a.createElement("p",null,n)))))}},177:function(e,a,t){e.exports=t.p+"static/media/ActivitiesLandingPage.da51c1f0.png"},237:function(e,a,t){e.exports=t.p+"static/media/outdore.4845f0ad.svg"},251:function(e,a,t){"use strict";t.r(a),t.d(a,"ActivitiesLink",function(){return S});var n=t(15),c=t.n(n),r=t(32),l=t(1),i=t(8),s=t.n(i),o=t(0),m=t.n(o),u=t(4),p=t(26),d=t(175),v=t(71),E=t(33),f=t(66),g=t(65),b=t(67),h=t(14),w=t(176),k=t(6),N=t(64),y=t(177),O=t.n(y),j=t(237),x=t.n(j),S=function(){var e=Object(u.g)().slug,a=Object(o.useState)(!1),t=Object(l.a)(a,2),n=t[0],i=t[1],y=Object(o.useState)(null),j=Object(l.a)(y,2),S=j[0],_=j[1],P=Object(o.useState)([]),C=Object(l.a)(P,2),L=C[0],F=C[1];Object(o.useEffect)(function(){(function(){var a=Object(r.a)(c.a.mark(function a(){var t;return c.a.wrap(function(a){for(;;)switch(a.prev=a.next){case 0:return i(!0),a.prev=1,a.next=4,s.a.get("".concat(k.b,"api/activities/activity/?slug=").concat(e));case 4:t=a.sent,_(t.data.item),a.next=11;break;case 8:a.prev=8,a.t0=a.catch(1),console.log(a.t0);case 11:i(!1);case 12:case"end":return a.stop()}},a,null,[[1,8]])}));return function(){return a.apply(this,arguments)}})()()},[e]),Object(o.useEffect)(function(){var e=new URLSearchParams;e.append("limit","4"),s.a.get("".concat(k.b,"api/activities/"),{params:e}).then(function(e){200===e.status&&F(e.data.data)}).catch(function(e){return console.log(e)})},[]);var A=Object(o.useState)({area:"",property:"",from:"",to:""}),M=Object(l.a)(A,2),G=M[0],R=M[1],T=Object(o.useState)([]),U=Object(l.a)(T,2),B=U[0],D=U[1],I=Object(o.useCallback)(function(){var e=new URLSearchParams;e.append("limit","4"),e.append("fromPrice",G.from),e.append("toPrice",G.to),e.append("area",G.area),s.a.get(k.b+"api/property/search/",{params:e}).then(function(e){console.log(e),200===e.status&&D(e.data.data)})},[G]);return Object(o.useEffect)(I,[]),m.a.createElement("div",{className:"activities-link-page-wrapper"},m.a.createElement(N.a,{coverImage:O.a,coverText:"a perfect mallorca day"},m.a.createElement("div",{className:"activities-link-page"},S&&m.a.createElement("div",{className:"explore-mallorca-activities-wrapper"},m.a.createElement(d.a,{icon:x.a,text:S.keywords[0],active:!0}),m.a.createElement(h.a,{text:S.details.title[0]}),m.a.createElement("div",{className:"rating"},[0,1,2,3,4].map(function(e){return m.a.createElement(g.a,{key:e,value:100*(S.rating.average-e),color:"#FFCB45"})}),m.a.createElement("p",null,S.rating.total," reviews ",m.a.createElement("span",null,"Palma, Spain"))),m.a.createElement("div",{className:"link-content"},m.a.createElement("div",{className:"row"},m.a.createElement("img",{src:S.thumbnail[0],alt:"link content"}),m.a.createElement("div",{className:"check"},m.a.createElement("h2",null,"From: ",m.a.createElement("span",null,"".concat(S.details.price_amount," ").concat(S.details.price_unit))),m.a.createElement("h6",null,"Lowest Price Guarantee"),m.a.createElement("h3",null,"Reserve Now & Pay Later"),m.a.createElement("p",null,"Secure your spot while staying flexible"),m.a.createElement("h3",null,"Free cancellation"),m.a.createElement("p",null,"Up to 24 hours in advance. ",m.a.createElement("a",{href:S.details.affiliate_link,target:"_blank",rel:"noopener noreferrer"},"Learn More")),m.a.createElement("a",{href:S.details.affiliate_link,target:"_blank",rel:"noopener noreferrer"},m.a.createElement("button",{className:n?"loading":""},"Check Availability"))),m.a.createElement("div",{className:"overview"},m.a.createElement("h4",null,"Overview"),m.a.createElement("p",null,S.details.long_desc[0]))))),m.a.createElement("div",{className:"top-activities-wrapper"},m.a.createElement(h.a,{text:"Top Activities in Mallorca"}),m.a.createElement("div",{className:"top-activities"},L.map(function(e,a){return m.a.createElement(v.a,{key:e.id,image:e.thumbnail[0],title:e.details.title[0],id:e.slug,price:"".concat(e.details.price_unit," ").concat(e.details.price_amount),rating:e.rating.average,ratingCount:e.rating.total})}))),m.a.createElement("div",{className:"top-attractions-wrapper"},m.a.createElement(h.a,{text:"Top 6 attractions in Mallorca"}),m.a.createElement("div",{className:"top-attractions"},k.c.map(function(e,a){return m.a.createElement(w.a,{key:e._id,img:e.src,desc:e.desc,title:e.title,value:e._id,rating:e.rating,slug:e.slug})}))),m.a.createElement(b.a,null),m.a.createElement("div",{className:"property-offers-wrapper"},m.a.createElement(h.a,{text:"Property Offers"}),m.a.createElement("div",{className:"property-offers"},m.a.createElement(f.a,{values:G,setValues:R,handleSubmit:I})),m.a.createElement("div",{className:"wrapper-slider"},m.a.createElement(E.a,{source:B,type:"props",secondGuideCardProp:!0}))),m.a.createElement("div",{className:"mallorca-gallery-images"},m.a.createElement(h.a,{text:"Mallorca Gallery"}),m.a.createElement("div",{className:"gallery-images"},m.a.createElement(p.a,{widgetID:"1b26b4ce-7ba2-4fb8-8e72-fdcdfa618769"}))))))};a.default=S}}]);
//# sourceMappingURL=8.f59632f4.chunk.js.map