(function e(t,n,r){function s(o,u){if(!n[o]){if(!t[o]){var a=typeof require=="function"&&require;if(!u&&a)return a(o,!0);if(i)return i(o,!0);var f=new Error("Cannot find module '"+o+"'");throw f.code="MODULE_NOT_FOUND",f}var l=n[o]={exports:{}};t[o][0].call(l.exports,function(e){var n=t[o][1][e];return s(n?n:e)},l,l.exports,e,t,n,r)}return n[o].exports}var i=typeof require=="function"&&require;for(var o=0;o<r.length;o++)s(r[o]);return s})({1:[function(require,module,exports){
require("./javascript/html5shiv"),require("./javascript/Array.isArray"),require("./javascript/Event"),require("./javascript/Array.prototype.every"),require("./javascript/Array.prototype.filter"),require("./javascript/Array.prototype.forEach"),require("./javascript/Array.prototype.indexOf"),require("./javascript/Array.prototype.map"),require("./javascript/Array.prototype.reduce"),require("./javascript/Date.now"),require("./javascript/Element.classList"),require("./javascript/Function.prototype.bind"),require("./javascript/Object.defineProperties"),require("./javascript/Object.defineProperty"),require("./javascript/Object.keys"),require("./javascript/String.prototype.trim"),require("./javascript/Window.prototype.matchMedia");
},{"./javascript/Array.isArray":2,"./javascript/Array.prototype.every":3,"./javascript/Array.prototype.filter":4,"./javascript/Array.prototype.forEach":5,"./javascript/Array.prototype.indexOf":6,"./javascript/Array.prototype.map":7,"./javascript/Array.prototype.reduce":8,"./javascript/Date.now":9,"./javascript/Element.classList":10,"./javascript/Event":11,"./javascript/Function.prototype.bind":12,"./javascript/Object.defineProperties":13,"./javascript/Object.defineProperty":14,"./javascript/Object.keys":15,"./javascript/String.prototype.trim":16,"./javascript/Window.prototype.matchMedia":17,"./javascript/html5shiv":18}],2:[function(require,module,exports){
"undefined"==typeof Array||Array.isArray||(Array.isArray=function(r){return r&&"[object Array]"===Object.prototype.toString.call(r)});

},{}],3:[function(require,module,exports){
Array.prototype.every||(Array.prototype.every=function(r,e){for(var t=this,o=0,y=t.length;y>o&&r.call(e||window,t[o],o,t);++o);return o===y});

},{}],4:[function(require,module,exports){
Array.prototype.filter||(Array.prototype.filter=function(r,t){for(var o,e=this,i=[],l=0,n=e.length;n>l;++l)o=e[l],r.call(t||window,o,l,e)&&i.push(o);return i});

},{}],5:[function(require,module,exports){
Array.prototype.forEach||(Array.prototype.forEach=function(r,o){for(var t=this,a=0,c=t.length;c>a;++a)r.call(o||window,t[a],a,t)});

},{}],6:[function(require,module,exports){
Array.prototype.indexOf||(Array.prototype.indexOf=function(r){for(var t=this,e=0,n=t.length;n>e;++e)if(t[e]===r)return e;return-1});

},{}],7:[function(require,module,exports){
Array.prototype.map||(Array.prototype.map=function(r,t){var n,o,e;if(null==this)throw new TypeError(" this is null or not defined");var i=Object(this),a=i.length>>>0;if("function"!=typeof r)throw new TypeError(r+" is not a function");for(arguments.length>1&&(n=t),o=new Array(a),e=0;a>e;){var p,f;e in i&&(p=i[e],f=r.call(n,p,e,i),o[e]=f),e++}return o});

},{}],8:[function(require,module,exports){
Array.prototype.reduce||(Array.prototype.reduce=function(r,e){for(var t=this,o=e||0,n=0,a=t.length;a>n;++n)o=r.call(window,o,t[n],n,t);return o});

},{}],9:[function(require,module,exports){
"undefined"==typeof Date||Date.now||(Date.now=function(){return(new Date).getTime()});

},{}],10:[function(require,module,exports){
"document"in self&&("classList"in document.createElement("_")?!function(){"use strict";var t=document.createElement("_");if(t.classList.add("c1","c2"),!t.classList.contains("c2")){var e=function(t){var e=DOMTokenList.prototype[t];DOMTokenList.prototype[t]=function(t){var n,i=arguments.length;for(n=0;i>n;n++)t=arguments[n],e.call(this,t)}};e("add"),e("remove")}if(t.classList.toggle("c3",!1),t.classList.contains("c3")){var n=DOMTokenList.prototype.toggle;DOMTokenList.prototype.toggle=function(t,e){return 1 in arguments&&!this.contains(t)==!e?e:n.call(this,t)}}t=null}():!function(t){"use strict";if("Element"in t){var e="classList",n="prototype",i=t.Element[n],s=Object,r=String[n].trim||function(){return this.replace(/^\s+|\s+$/g,"")},o=Array[n].indexOf||function(t){for(var e=0,n=this.length;n>e;e++)if(e in this&&this[e]===t)return e;return-1},a=function(t,e){this.name=t,this.code=DOMException[t],this.message=e},c=function(t,e){if(""===e)throw new a("SYNTAX_ERR","An invalid or illegal string was specified");if(/\s/.test(e))throw new a("INVALID_CHARACTER_ERR","String contains an invalid character");return o.call(t,e)},l=function(t){for(var e=r.call(t.getAttribute("class")||""),n=e?e.split(/\s+/):[],i=0,s=n.length;s>i;i++)this.push(n[i]);this._updateClassName=function(){t.setAttribute("class",this.toString())}},u=l[n]=[],f=function(){return new l(this)};if(a[n]=Error[n],u.item=function(t){return this[t]||null},u.contains=function(t){return t+="",-1!==c(this,t)},u.add=function(){var t,e=arguments,n=0,i=e.length,s=!1;do t=e[n]+"",-1===c(this,t)&&(this.push(t),s=!0);while(++n<i);s&&this._updateClassName()},u.remove=function(){var t,e,n=arguments,i=0,s=n.length,r=!1;do for(t=n[i]+"",e=c(this,t);-1!==e;)this.splice(e,1),r=!0,e=c(this,t);while(++i<s);r&&this._updateClassName()},u.toggle=function(t,e){t+="";var n=this.contains(t),i=n?e!==!0&&"remove":e!==!1&&"add";return i&&this[i](t),e===!0||e===!1?e:!n},u.toString=function(){return this.join(" ")},s.defineProperty){var h={get:f,enumerable:!0,configurable:!0};try{s.defineProperty(i,e,h)}catch(d){-2146823252===d.number&&(h.enumerable=!1,s.defineProperty(i,e,h))}}else s[n].__defineGetter__&&i.__defineGetter__(e,f)}}(self));

},{}],11:[function(require,module,exports){
!function(){if(Event.prototype.preventDefault||(Event.prototype.preventDefault=function(){this.returnValue=!1}),Event.prototype.stopPropagation||(Event.prototype.stopPropagation=function(){this.cancelBubble=!0}),!Element.prototype.addEventListener){var e=[],t=function(t,n){var o=this,r=function(e){e.target=e.srcElement,e.currentTarget=o,"undefined"!=typeof n.handleEvent?n.handleEvent(e):n.call(o,e)};if("DOMContentLoaded"==t){var a=function(e){"complete"==document.readyState&&r(e)};if(document.attachEvent("onreadystatechange",a),e.push({object:this,type:t,listener:n,wrapper:a}),"complete"==document.readyState){var p=new Event;p.srcElement=window,a(p)}}else this.attachEvent("on"+t,r),e.push({object:this,type:t,listener:n,wrapper:r})},n=function(t,n){for(var o=0;o<e.length;){var r=e[o];if(r.object==this&&r.type==t&&r.listener==n){"DOMContentLoaded"==t?this.detachEvent("onreadystatechange",r.wrapper):this.detachEvent("on"+t,r.wrapper),e.splice(o,1);break}++o}};Element.prototype.addEventListener=t,Element.prototype.removeEventListener=n,HTMLDocument&&(HTMLDocument.prototype.addEventListener=t,HTMLDocument.prototype.removeEventListener=n),Window&&(Window.prototype.addEventListener=t,Window.prototype.removeEventListener=n)}}();

},{}],12:[function(require,module,exports){
Function.prototype.bind||(Function.prototype.bind=function(t){var o=this,n=Array.prototype.slice.call(arguments,1),p=function(){},r=function(){return o.apply(this instanceof p&&t?this:t,n.concat(Array.prototype.slice.call(arguments,0)))};return p.prototype=r.prototype=o.prototype,r});

},{}],13:[function(require,module,exports){
"undefined"==typeof Object||Object.defineProperties||(Object.defineProperties=function(e,r){for(var t in r)Object.defineProperty(e,t,r[t]);return e});

},{}],14:[function(require,module,exports){
"undefined"==typeof Object||Object.defineProperty||(Object.defineProperty=function(e,t,n){return n.get&&e.__defineGetter__(t,n.get),n.set&&e.__defineSetter__(t,n.set),e});

},{}],15:[function(require,module,exports){
"undefined"==typeof Object||Object.keys||(Object.keys=function(e){var t,n=[];for(t in e)Object.prototype.hasOwnProperty.call(e,t)&&n.push(t);return n});

},{}],16:[function(require,module,exports){
String.prototype.trim||(String.prototype.trim=function(){return this.replace(/^\s+|\s+$/g,"")});

},{}],17:[function(require,module,exports){
"undefined"==typeof window.matchMedia&&!function(){function e(e,t){return new Function("media","try{ return !!(%s) }catch(e){ return false }".replace("%s",t||"true").replace(/^only\s+/,"").replace(/(device)-([\w.]+)/g,"$1.$2").replace(/([\w.]+)\s*:/g,"media.$1 ===").replace(/min-([\w.]+)\s*===/g,"$1 >=").replace(/max-([\w.]+)\s*===/g,"$1 <=").replace(/all|screen/g,"1").replace(/print/g,"0").replace(/,/g,"||").replace(/and/g,"&&").replace(/dpi/g,"").replace(/(\d+)(cm|em|in|mm|pc|pt|px|rem)/,function(e,t,n){return t*("cm"===n?37.7952:"em"===n||"rem"===n?16:"in"===n?96:"mm"===n?3.77952:"pc"===n?16:"pt"===n?96/72:1)}))({width:e.innerWidth,height:e.innerHeight,orientation:e.orientation||"landscape",device:{width:e.screen.width,height:e.screen.height,orientation:e.screen.orientation||e.orientation||"landscape"}})}function t(){this.matches=!1,this.media="invalid"}t.prototype.addListener=function(e){this.addListener.listeners.push(e)},t.prototype.removeListener=function(e){this.addListener.listeners.splice(this.addListener.listeners.indexof(e),1)},window.matchMedia=Window.prototype.matchMedia=function(n){var i=this,r=new t;if(0===arguments.length)throw new TypeError("Not enough arguments to window.matchMedia");return r.media=String(n),r.matches=e(i,r.media),r.addListener.listeners=[],i.addEventListener("resize",function(){var t=[].concat(r.addListener.listeners),n=e(i,r.media);if(n!=r.matches){r.matches=n;for(var a=0,c=t.length;c>a;++a)t[a].call(i,r)}}),r}}();

},{}],18:[function(require,module,exports){
var elements="abbr article aside audio bdi canvas data datalist details figcaption figure footer header hgroup main mark meter nav output progress section summary template time video".split(" ");for(var i in elements)elements.hasOwnProperty(i)&&document.createElement(elements[i]);

},{}]},{},[1]);
