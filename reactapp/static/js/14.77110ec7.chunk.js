(window.webpackJsonp=window.webpackJsonp||[]).push([[14],{171:function(e,t,a){e.exports=a.p+"static/media/sms.2c09bd0e.svg"},172:function(e,t,a){e.exports=a.p+"static/media/login.a9ced1f7.png"},253:function(e,t,a){"use strict";a.r(t);var n=a(1),r=a(8),s=a.n(r),c=a(0),o=a.n(c),l=a(2),i=a(14),u=a(6),d=a(64),m=a(172),p=a.n(m),b=a(171),w=a.n(b),E=a(72);t.default=function(){var e=Object(c.useState)(""),t=Object(n.a)(e,2),a=t[0],r=t[1],m=Object(c.useState)(!1),b=Object(n.a)(m,2),v=b[0],y=b[1],f=Object(c.useState)(!1),g=Object(n.a)(f,2),j=g[0],O=g[1],h=Object(c.useState)(""),N=Object(n.a)(h,2),x=N[0],k=N[1],S=Object(c.useCallback)(function(){O(!0),k("");var e="".concat(u.b,"api/accounts/password_reset/");s.a.post(e,{email:a}).then(function(e){200===e.status?(k("Please check your email to reset your password."),r("")):k("Unknown error. Please try agauint later.")}).catch(function(e){return k(e.response.data.email)}).finally(function(){return O(!1)})},[a]);return Object(c.useEffect)(function(){y(Object(E.a)(a))},[a]),o.a.createElement("div",{className:"login-screen-wrapper"},o.a.createElement(d.a,{coverImage:p.a,coverText:"Welcome to Mallorca Magic"},o.a.createElement("div",{className:"login-wrapper"},o.a.createElement("div",null,o.a.createElement(i.a,{text:"Reset your password"}),x&&o.a.createElement("div",{className:"error"},x),o.a.createElement("div",{className:"login"},o.a.createElement("p",{style:{textAlign:"center"}},"Enter the email address you used when you joined and we\u2019ll send you instructions to reset your password."),o.a.createElement("p",{style:{textAlign:"center"}},"For security reasons, we do NOT store your password. So rest assured that we will never send your password via email."),o.a.createElement("label",null,"Email"),o.a.createElement("div",{className:"input"},o.a.createElement(l.a,{src:w.a}),o.a.createElement("input",{type:"text",placeholder:"Type your Email address",value:a,onChange:function(e){return r(e.target.value)}})),o.a.createElement("div",{className:"buttons"},o.a.createElement("button",{onClick:S,className:j?"loading reset-button":"reset-button",disabled:j||!v},"Send reset instructiion")))))))}}}]);
//# sourceMappingURL=14.77110ec7.chunk.js.map