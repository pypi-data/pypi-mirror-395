"use strict";
(self["webpackChunkjupyterlab_chat_toy"] = self["webpackChunkjupyterlab_chat_toy"] || []).push([["style_index_css"],{

/***/ "./node_modules/css-loader/dist/cjs.js!./style/index.css":
/*!***************************************************************!*\
  !*** ./node_modules/css-loader/dist/cjs.js!./style/index.css ***!
  \***************************************************************/
/***/ ((module, __webpack_exports__, __webpack_require__) => {

__webpack_require__.r(__webpack_exports__);
/* harmony export */ __webpack_require__.d(__webpack_exports__, {
/* harmony export */   "default": () => (__WEBPACK_DEFAULT_EXPORT__)
/* harmony export */ });
/* harmony import */ var _node_modules_css_loader_dist_runtime_cssWithMappingToString_js__WEBPACK_IMPORTED_MODULE_0__ = __webpack_require__(/*! ../node_modules/css-loader/dist/runtime/cssWithMappingToString.js */ "./node_modules/css-loader/dist/runtime/cssWithMappingToString.js");
/* harmony import */ var _node_modules_css_loader_dist_runtime_cssWithMappingToString_js__WEBPACK_IMPORTED_MODULE_0___default = /*#__PURE__*/__webpack_require__.n(_node_modules_css_loader_dist_runtime_cssWithMappingToString_js__WEBPACK_IMPORTED_MODULE_0__);
/* harmony import */ var _node_modules_css_loader_dist_runtime_api_js__WEBPACK_IMPORTED_MODULE_1__ = __webpack_require__(/*! ../node_modules/css-loader/dist/runtime/api.js */ "./node_modules/css-loader/dist/runtime/api.js");
/* harmony import */ var _node_modules_css_loader_dist_runtime_api_js__WEBPACK_IMPORTED_MODULE_1___default = /*#__PURE__*/__webpack_require__.n(_node_modules_css_loader_dist_runtime_api_js__WEBPACK_IMPORTED_MODULE_1__);
// Imports


var ___CSS_LOADER_EXPORT___ = _node_modules_css_loader_dist_runtime_api_js__WEBPACK_IMPORTED_MODULE_1___default()((_node_modules_css_loader_dist_runtime_cssWithMappingToString_js__WEBPACK_IMPORTED_MODULE_0___default()));
// Module
___CSS_LOADER_EXPORT___.push([module.id, "/* 确保聊天界面适应JupyterLab主题 */\r\n.jp-ChatWidget {\r\n  height: 100%;\r\n  display: flex;\r\n  flex-direction: column;\r\n}\r\n\r\n/* 消息滚动区域 */\r\n.jp-ChatMessages {\r\n  flex: 1;\r\n  overflow-y: auto;\r\n  padding: 8px;\r\n}\r\n\r\n/* 输入区域 */\r\n.jp-ChatInput {\r\n  border-top: 1px solid var(--jp-border-color1);\r\n  padding: 8px;\r\n  background: var(--jp-layout-color1);\r\n}\r\n\r\n/* 代码块样式 */\r\n.jp-ChatCodeBlock {\r\n  margin: 8px 0;\r\n  border-radius: 4px;\r\n  overflow: hidden;\r\n}\r\n\r\n/* 消息气泡 */\r\n.jp-ChatMessage-bubble {\r\n  max-width: 70%;\r\n  padding: 8px 12px;\r\n  border-radius: 12px;\r\n  margin: 4px 0;\r\n  word-wrap: break-word;\r\n}\r\n\r\n.jp-ChatMessage-user {\r\n  background: var(--jp-brand-color1);\r\n  color: white;\r\n  margin-left: auto;\r\n}\r\n\r\n.jp-ChatMessage-ai {\r\n  background: var(--jp-layout-color2);\r\n  color: var(--jp-ui-font-color1);\r\n}", "",{"version":3,"sources":["webpack://./style/index.css"],"names":[],"mappings":"AAAA,yBAAyB;AACzB;EACE,YAAY;EACZ,aAAa;EACb,sBAAsB;AACxB;;AAEA,WAAW;AACX;EACE,OAAO;EACP,gBAAgB;EAChB,YAAY;AACd;;AAEA,SAAS;AACT;EACE,6CAA6C;EAC7C,YAAY;EACZ,mCAAmC;AACrC;;AAEA,UAAU;AACV;EACE,aAAa;EACb,kBAAkB;EAClB,gBAAgB;AAClB;;AAEA,SAAS;AACT;EACE,cAAc;EACd,iBAAiB;EACjB,mBAAmB;EACnB,aAAa;EACb,qBAAqB;AACvB;;AAEA;EACE,kCAAkC;EAClC,YAAY;EACZ,iBAAiB;AACnB;;AAEA;EACE,mCAAmC;EACnC,+BAA+B;AACjC","sourcesContent":["/* 确保聊天界面适应JupyterLab主题 */\r\n.jp-ChatWidget {\r\n  height: 100%;\r\n  display: flex;\r\n  flex-direction: column;\r\n}\r\n\r\n/* 消息滚动区域 */\r\n.jp-ChatMessages {\r\n  flex: 1;\r\n  overflow-y: auto;\r\n  padding: 8px;\r\n}\r\n\r\n/* 输入区域 */\r\n.jp-ChatInput {\r\n  border-top: 1px solid var(--jp-border-color1);\r\n  padding: 8px;\r\n  background: var(--jp-layout-color1);\r\n}\r\n\r\n/* 代码块样式 */\r\n.jp-ChatCodeBlock {\r\n  margin: 8px 0;\r\n  border-radius: 4px;\r\n  overflow: hidden;\r\n}\r\n\r\n/* 消息气泡 */\r\n.jp-ChatMessage-bubble {\r\n  max-width: 70%;\r\n  padding: 8px 12px;\r\n  border-radius: 12px;\r\n  margin: 4px 0;\r\n  word-wrap: break-word;\r\n}\r\n\r\n.jp-ChatMessage-user {\r\n  background: var(--jp-brand-color1);\r\n  color: white;\r\n  margin-left: auto;\r\n}\r\n\r\n.jp-ChatMessage-ai {\r\n  background: var(--jp-layout-color2);\r\n  color: var(--jp-ui-font-color1);\r\n}"],"sourceRoot":""}]);
// Exports
/* harmony default export */ const __WEBPACK_DEFAULT_EXPORT__ = (___CSS_LOADER_EXPORT___);


/***/ }),

/***/ "./style/index.css":
/*!*************************!*\
  !*** ./style/index.css ***!
  \*************************/
/***/ ((__unused_webpack_module, __webpack_exports__, __webpack_require__) => {

__webpack_require__.r(__webpack_exports__);
/* harmony export */ __webpack_require__.d(__webpack_exports__, {
/* harmony export */   "default": () => (__WEBPACK_DEFAULT_EXPORT__)
/* harmony export */ });
/* harmony import */ var _node_modules_style_loader_dist_runtime_injectStylesIntoStyleTag_js__WEBPACK_IMPORTED_MODULE_0__ = __webpack_require__(/*! !../node_modules/style-loader/dist/runtime/injectStylesIntoStyleTag.js */ "./node_modules/style-loader/dist/runtime/injectStylesIntoStyleTag.js");
/* harmony import */ var _node_modules_style_loader_dist_runtime_injectStylesIntoStyleTag_js__WEBPACK_IMPORTED_MODULE_0___default = /*#__PURE__*/__webpack_require__.n(_node_modules_style_loader_dist_runtime_injectStylesIntoStyleTag_js__WEBPACK_IMPORTED_MODULE_0__);
/* harmony import */ var _node_modules_css_loader_dist_cjs_js_index_css__WEBPACK_IMPORTED_MODULE_1__ = __webpack_require__(/*! !!../node_modules/css-loader/dist/cjs.js!./index.css */ "./node_modules/css-loader/dist/cjs.js!./style/index.css");

            

var options = {};

options.insert = "head";
options.singleton = false;

var update = _node_modules_style_loader_dist_runtime_injectStylesIntoStyleTag_js__WEBPACK_IMPORTED_MODULE_0___default()(_node_modules_css_loader_dist_cjs_js_index_css__WEBPACK_IMPORTED_MODULE_1__["default"], options);



/* harmony default export */ const __WEBPACK_DEFAULT_EXPORT__ = (_node_modules_css_loader_dist_cjs_js_index_css__WEBPACK_IMPORTED_MODULE_1__["default"].locals || {});

/***/ })

}]);
//# sourceMappingURL=style_index_css.a0d180866364f95a0643.js.map