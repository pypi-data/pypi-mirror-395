"use strict";
(self["webpackChunkpret"] = self["webpackChunkpret"] || []).push([["client_index_tsx"],{

/***/ "./client/globals.ts":
/*!***************************!*\
  !*** ./client/globals.ts ***!
  \***************************/
/***/ ((__unused_webpack_module, __unused_webpack___webpack_exports__, __webpack_require__) => {

/* harmony import */ var _routing__WEBPACK_IMPORTED_MODULE_0__ = __webpack_require__(/*! ./routing */ "./client/routing.tsx");

window.PretRouter = { 'HashRouter': _routing__WEBPACK_IMPORTED_MODULE_0__.HashRouter, 'BrowserRouter': _routing__WEBPACK_IMPORTED_MODULE_0__.BrowserRouter, 'Route': _routing__WEBPACK_IMPORTED_MODULE_0__.Route, 'Routes': _routing__WEBPACK_IMPORTED_MODULE_0__.Routes, 'useMatch': _routing__WEBPACK_IMPORTED_MODULE_0__.useMatch, 'useSearchParams': _routing__WEBPACK_IMPORTED_MODULE_0__.useSearchParams, 'useLocation': _routing__WEBPACK_IMPORTED_MODULE_0__.useLocation, 'useParams': _routing__WEBPACK_IMPORTED_MODULE_0__.useParams, 'Outlet': _routing__WEBPACK_IMPORTED_MODULE_0__.Outlet };


/***/ }),

/***/ "./client/index.tsx":
/*!**************************!*\
  !*** ./client/index.tsx ***!
  \**************************/
/***/ ((__unused_webpack_module, __webpack_exports__, __webpack_require__) => {

__webpack_require__.r(__webpack_exports__);
/* harmony import */ var _pret_globals__WEBPACK_IMPORTED_MODULE_0__ = __webpack_require__(/*! @pret-globals */ "./client/globals.ts");



/***/ }),

/***/ "./client/routing.tsx":
/*!****************************!*\
  !*** ./client/routing.tsx ***!
  \****************************/
/***/ ((__unused_webpack_module, __webpack_exports__, __webpack_require__) => {

/* harmony export */ __webpack_require__.d(__webpack_exports__, {
/* harmony export */   BrowserRouter: () => (/* binding */ BrowserRouter),
/* harmony export */   HashRouter: () => (/* binding */ HashRouter),
/* harmony export */   Outlet: () => (/* reexport safe */ react_router__WEBPACK_IMPORTED_MODULE_1__.Outlet),
/* harmony export */   Route: () => (/* reexport safe */ react_router__WEBPACK_IMPORTED_MODULE_1__.Route),
/* harmony export */   Routes: () => (/* reexport safe */ react_router__WEBPACK_IMPORTED_MODULE_1__.Routes),
/* harmony export */   useLocation: () => (/* reexport safe */ react_router__WEBPACK_IMPORTED_MODULE_1__.useLocation),
/* harmony export */   useMatch: () => (/* reexport safe */ react_router__WEBPACK_IMPORTED_MODULE_1__.useMatch),
/* harmony export */   useParams: () => (/* reexport safe */ react_router__WEBPACK_IMPORTED_MODULE_1__.useParams),
/* harmony export */   useSearchParams: () => (/* reexport safe */ react_router_dom__WEBPACK_IMPORTED_MODULE_2__.useSearchParams)
/* harmony export */ });
/* unused harmony export useInterceptAnchorsClicks */
/* harmony import */ var react_jsx_runtime__WEBPACK_IMPORTED_MODULE_0__ = __webpack_require__(/*! react/jsx-runtime */ "./node_modules/react/jsx-runtime.js");
/* harmony import */ var react_router__WEBPACK_IMPORTED_MODULE_1__ = __webpack_require__(/*! react-router */ "webpack/sharing/consume/default/react-router/react-router?81bf");
/* harmony import */ var react_router__WEBPACK_IMPORTED_MODULE_1___default = /*#__PURE__*/__webpack_require__.n(react_router__WEBPACK_IMPORTED_MODULE_1__);
/* harmony import */ var react_router_dom__WEBPACK_IMPORTED_MODULE_2__ = __webpack_require__(/*! react-router-dom */ "webpack/sharing/consume/default/react-router-dom/react-router-dom");
/* harmony import */ var react_router_dom__WEBPACK_IMPORTED_MODULE_2___default = /*#__PURE__*/__webpack_require__.n(react_router_dom__WEBPACK_IMPORTED_MODULE_2__);
/* harmony import */ var react__WEBPACK_IMPORTED_MODULE_3__ = __webpack_require__(/*! react */ "webpack/sharing/consume/default/react");
/* harmony import */ var react__WEBPACK_IMPORTED_MODULE_3___default = /*#__PURE__*/__webpack_require__.n(react__WEBPACK_IMPORTED_MODULE_3__);
var __rest = (undefined && undefined.__rest) || function (s, e) {
    var t = {};
    for (var p in s) if (Object.prototype.hasOwnProperty.call(s, p) && e.indexOf(p) < 0)
        t[p] = s[p];
    if (s != null && typeof Object.getOwnPropertySymbols === "function")
        for (var i = 0, p = Object.getOwnPropertySymbols(s); i < p.length; i++) {
            if (e.indexOf(p[i]) < 0 && Object.prototype.propertyIsEnumerable.call(s, p[i]))
                t[p[i]] = s[p[i]];
        }
    return t;
};






function useInterceptAnchorsClicks({ containerRef, basename = "", exclude_attr = "data-router-ignore", } = {}) {
    const navigate = (0,react_router_dom__WEBPACK_IMPORTED_MODULE_2__.useNavigate)();
    (0,react__WEBPACK_IMPORTED_MODULE_3__.useEffect)(() => {
        const root = containerRef === null || containerRef === void 0 ? void 0 : containerRef.current;
        if (!root)
            return;
        const onClick = (e) => {
            var _a, _b;
            if (e.defaultPrevented || e.button !== 0)
                return;
            if (e.metaKey || e.ctrlKey || e.shiftKey || e.altKey)
                return;
            const a = (_b = (_a = e.target) === null || _a === void 0 ? void 0 : _a.closest) === null || _b === void 0 ? void 0 : _b.call(_a, "a[href]");
            if (!a)
                return;
            if (a.hasAttribute(exclude_attr))
                return;
            if (a.hasAttribute("download"))
                return;
            const tgt = (a.getAttribute("target") || "").toLowerCase();
            if (tgt && tgt !== "_self")
                return;
            if ((a.getAttribute("rel") || "").includes("external"))
                return;
            const href = a.getAttribute("href") || "";
            if (href.startsWith("#"))
                return;
            if (/^(mailto|tel|ftp|blob|data|javascript):/i.test(href))
                return;
            const url = new URL(href, window.location.href);
            if (url.origin !== window.location.origin)
                return;
            // get the rel path
            let pathname = url.pathname;
            if (basename && pathname.startsWith(basename)) {
                pathname = pathname.slice(basename.length) || "/";
            }
            e.preventDefault();
            navigate(pathname + url.search + url.hash);
        };
        // capture to handle the click before other handles
        root.addEventListener("click", onClick, { capture: true });
        return () => root.removeEventListener("click", onClick, { capture: true });
    }, [navigate, containerRef, basename, exclude_attr]);
}
function AnchorClickInterceptor(props) {
    useInterceptAnchorsClicks(props);
    return null;
}
function BrowserRouter(props) {
    const { interceptAnchorClicks, children } = props, rest = __rest(props, ["interceptAnchorClicks", "children"]);
    if (!interceptAnchorClicks) {
        return (0,react_jsx_runtime__WEBPACK_IMPORTED_MODULE_0__.jsx)(react_router_dom__WEBPACK_IMPORTED_MODULE_2__.BrowserRouter, Object.assign({}, rest, { children: children }));
    }
    const containerRef = (0,react__WEBPACK_IMPORTED_MODULE_3__.useRef)(null);
    const basename = (typeof interceptAnchorClicks === "object" &&
        interceptAnchorClicks.basename) ||
        props.basename ||
        "";
    const exclude_attr = (typeof interceptAnchorClicks === "object" &&
        interceptAnchorClicks.exclude_attr) ||
        "data-router-ignore";
    return ((0,react_jsx_runtime__WEBPACK_IMPORTED_MODULE_0__.jsxs)(react_router_dom__WEBPACK_IMPORTED_MODULE_2__.BrowserRouter, Object.assign({ future: { v7_startTransition: true } }, rest, { children: [(0,react_jsx_runtime__WEBPACK_IMPORTED_MODULE_0__.jsx)(AnchorClickInterceptor, { containerRef: containerRef, basename: basename, exclude_attr: exclude_attr }), (0,react_jsx_runtime__WEBPACK_IMPORTED_MODULE_0__.jsx)("div", { ref: containerRef, children: children })] })));
}
function HashRouter(props) {
    const { interceptAnchorClicks, children } = props, rest = __rest(props, ["interceptAnchorClicks", "children"]);
    if (!interceptAnchorClicks) {
        return (0,react_jsx_runtime__WEBPACK_IMPORTED_MODULE_0__.jsx)(react_router_dom__WEBPACK_IMPORTED_MODULE_2__.HashRouter, Object.assign({}, rest, { children: children }));
    }
    const containerRef = (0,react__WEBPACK_IMPORTED_MODULE_3__.useRef)(null);
    const basename = (typeof interceptAnchorClicks === "object" &&
        interceptAnchorClicks.basename) ||
        props.basename ||
        "";
    const exclude_attr = (typeof interceptAnchorClicks === "object" &&
        interceptAnchorClicks.exclude_attr) ||
        "data-router-ignore";
    return ((0,react_jsx_runtime__WEBPACK_IMPORTED_MODULE_0__.jsxs)(react_router_dom__WEBPACK_IMPORTED_MODULE_2__.HashRouter, Object.assign({ future: { v7_startTransition: true } }, rest, { children: [(0,react_jsx_runtime__WEBPACK_IMPORTED_MODULE_0__.jsx)(AnchorClickInterceptor, { containerRef: containerRef, basename: basename, exclude_attr: exclude_attr }), (0,react_jsx_runtime__WEBPACK_IMPORTED_MODULE_0__.jsx)("div", { ref: containerRef, children: children })] })));
}


/***/ })

}]);
//# sourceMappingURL=client_index_tsx.babee5811e387252fdce.js.map