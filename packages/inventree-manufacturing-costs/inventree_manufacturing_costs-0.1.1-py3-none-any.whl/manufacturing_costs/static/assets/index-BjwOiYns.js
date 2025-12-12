var __typeError = (msg) => {
  throw TypeError(msg);
};
var __accessCheck = (obj, member, msg) => member.has(obj) || __typeError("Cannot " + msg);
var __privateGet = (obj, member, getter) => (__accessCheck(obj, member, "read from private field"), getter ? getter.call(obj) : member.get(obj));
var __privateAdd = (obj, member, value) => member.has(obj) ? __typeError("Cannot add the same private member more than once") : member instanceof WeakSet ? member.add(obj) : member.set(obj, value);
var __privateSet = (obj, member, value, setter) => (__accessCheck(obj, member, "write to private field"), setter ? setter.call(obj, value) : member.set(obj, value), value);
var __privateMethod = (obj, member, method) => (__accessCheck(obj, member, "access private method"), method);
var _focused, _cleanup, _setup, _a, _online, _cleanup2, _setup2, _b, _client, _currentQuery, _currentQueryInitialState, _currentResult, _currentResultState, _currentResultOptions, _currentThenable, _selectError, _selectFn, _selectResult, _lastQueryWithDefinedData, _staleTimeoutId, _refetchIntervalId, _currentRefetchInterval, _trackedProps, _QueryObserver_instances, executeFetch_fn, updateStaleTimeout_fn, computeRefetchInterval_fn, updateRefetchInterval_fn, updateTimers_fn, clearStaleTimeout_fn, clearRefetchInterval_fn, updateQuery_fn, notify_fn, _c;
const INVENTREE_PLUGIN_VERSION = "0.5.1";
var ApiEndpoints = /* @__PURE__ */ ((ApiEndpoints2) => {
  ApiEndpoints2["api_server_info"] = "";
  ApiEndpoints2["user_list"] = "user/";
  ApiEndpoints2["user_set_password"] = "user/:id/set-password/";
  ApiEndpoints2["user_me"] = "user/me/";
  ApiEndpoints2["user_profile"] = "user/profile/";
  ApiEndpoints2["user_roles"] = "user/roles/";
  ApiEndpoints2["user_token"] = "user/token/";
  ApiEndpoints2["user_tokens"] = "user/tokens/";
  ApiEndpoints2["user_simple_login"] = "email/generate/";
  ApiEndpoints2["user_reset"] = "auth/v1/auth/password/request";
  ApiEndpoints2["user_reset_set"] = "auth/v1/auth/password/reset";
  ApiEndpoints2["auth_pwd_change"] = "auth/v1/account/password/change";
  ApiEndpoints2["auth_login"] = "auth/v1/auth/login";
  ApiEndpoints2["auth_login_2fa"] = "auth/v1/auth/2fa/authenticate";
  ApiEndpoints2["auth_session"] = "auth/v1/auth/session";
  ApiEndpoints2["auth_signup"] = "auth/v1/auth/signup";
  ApiEndpoints2["auth_authenticators"] = "auth/v1/account/authenticators";
  ApiEndpoints2["auth_recovery"] = "auth/v1/account/authenticators/recovery-codes";
  ApiEndpoints2["auth_mfa_reauthenticate"] = "auth/v1/auth/2fa/reauthenticate";
  ApiEndpoints2["auth_totp"] = "auth/v1/account/authenticators/totp";
  ApiEndpoints2["auth_trust"] = "auth/v1/auth/2fa/trust";
  ApiEndpoints2["auth_reauthenticate"] = "auth/v1/auth/reauthenticate";
  ApiEndpoints2["auth_email"] = "auth/v1/account/email";
  ApiEndpoints2["auth_email_verify"] = "auth/v1/auth/email/verify";
  ApiEndpoints2["auth_providers"] = "auth/v1/account/providers";
  ApiEndpoints2["auth_provider_redirect"] = "auth/v1/auth/provider/redirect";
  ApiEndpoints2["auth_config"] = "auth/v1/config";
  ApiEndpoints2["currency_list"] = "currency/exchange/";
  ApiEndpoints2["currency_refresh"] = "currency/refresh/";
  ApiEndpoints2["all_units"] = "units/all/";
  ApiEndpoints2["task_overview"] = "background-task/";
  ApiEndpoints2["task_pending_list"] = "background-task/pending/";
  ApiEndpoints2["task_scheduled_list"] = "background-task/scheduled/";
  ApiEndpoints2["task_failed_list"] = "background-task/failed/";
  ApiEndpoints2["api_search"] = "search/";
  ApiEndpoints2["settings_global_list"] = "settings/global/";
  ApiEndpoints2["settings_user_list"] = "settings/user/";
  ApiEndpoints2["news"] = "news/";
  ApiEndpoints2["global_status"] = "generic/status/";
  ApiEndpoints2["custom_state_list"] = "generic/status/custom/";
  ApiEndpoints2["version"] = "version/";
  ApiEndpoints2["license"] = "license/";
  ApiEndpoints2["group_list"] = "user/group/";
  ApiEndpoints2["owner_list"] = "user/owner/";
  ApiEndpoints2["ruleset_list"] = "user/ruleset/";
  ApiEndpoints2["content_type_list"] = "contenttype/";
  ApiEndpoints2["icons"] = "icons/";
  ApiEndpoints2["selectionlist_list"] = "selection/";
  ApiEndpoints2["selectionlist_detail"] = "selection/:id/";
  ApiEndpoints2["barcode"] = "barcode/";
  ApiEndpoints2["barcode_history"] = "barcode/history/";
  ApiEndpoints2["barcode_link"] = "barcode/link/";
  ApiEndpoints2["barcode_unlink"] = "barcode/unlink/";
  ApiEndpoints2["barcode_generate"] = "barcode/generate/";
  ApiEndpoints2["data_output"] = "data-output/";
  ApiEndpoints2["import_session_list"] = "importer/session/";
  ApiEndpoints2["import_session_accept_fields"] = "importer/session/:id/accept_fields/";
  ApiEndpoints2["import_session_accept_rows"] = "importer/session/:id/accept_rows/";
  ApiEndpoints2["import_session_column_mapping_list"] = "importer/column-mapping/";
  ApiEndpoints2["import_session_row_list"] = "importer/row/";
  ApiEndpoints2["notifications_list"] = "notifications/";
  ApiEndpoints2["notifications_readall"] = "notifications/readall/";
  ApiEndpoints2["build_order_list"] = "build/";
  ApiEndpoints2["build_order_issue"] = "build/:id/issue/";
  ApiEndpoints2["build_order_cancel"] = "build/:id/cancel/";
  ApiEndpoints2["build_order_hold"] = "build/:id/hold/";
  ApiEndpoints2["build_order_complete"] = "build/:id/finish/";
  ApiEndpoints2["build_output_complete"] = "build/:id/complete/";
  ApiEndpoints2["build_output_create"] = "build/:id/create-output/";
  ApiEndpoints2["build_output_scrap"] = "build/:id/scrap-outputs/";
  ApiEndpoints2["build_output_delete"] = "build/:id/delete-outputs/";
  ApiEndpoints2["build_order_auto_allocate"] = "build/:id/auto-allocate/";
  ApiEndpoints2["build_order_allocate"] = "build/:id/allocate/";
  ApiEndpoints2["build_order_consume"] = "build/:id/consume/";
  ApiEndpoints2["build_order_deallocate"] = "build/:id/unallocate/";
  ApiEndpoints2["build_line_list"] = "build/line/";
  ApiEndpoints2["build_item_list"] = "build/item/";
  ApiEndpoints2["bom_list"] = "bom/";
  ApiEndpoints2["bom_item_validate"] = "bom/:id/validate/";
  ApiEndpoints2["bom_validate"] = "part/:id/bom-validate/";
  ApiEndpoints2["bom_substitute_list"] = "bom/substitute/";
  ApiEndpoints2["part_list"] = "part/";
  ApiEndpoints2["part_parameter_list"] = "part/parameter/";
  ApiEndpoints2["part_parameter_template_list"] = "part/parameter/template/";
  ApiEndpoints2["part_thumbs_list"] = "part/thumbs/";
  ApiEndpoints2["part_pricing"] = "part/:id/pricing/";
  ApiEndpoints2["part_requirements"] = "part/:id/requirements/";
  ApiEndpoints2["part_serial_numbers"] = "part/:id/serial-numbers/";
  ApiEndpoints2["part_scheduling"] = "part/:id/scheduling/";
  ApiEndpoints2["part_pricing_internal"] = "part/internal-price/";
  ApiEndpoints2["part_pricing_sale"] = "part/sale-price/";
  ApiEndpoints2["part_stocktake_list"] = "part/stocktake/";
  ApiEndpoints2["category_list"] = "part/category/";
  ApiEndpoints2["category_tree"] = "part/category/tree/";
  ApiEndpoints2["category_parameter_list"] = "part/category/parameters/";
  ApiEndpoints2["related_part_list"] = "part/related/";
  ApiEndpoints2["part_test_template_list"] = "part/test-template/";
  ApiEndpoints2["company_list"] = "company/";
  ApiEndpoints2["contact_list"] = "company/contact/";
  ApiEndpoints2["address_list"] = "company/address/";
  ApiEndpoints2["supplier_part_list"] = "company/part/";
  ApiEndpoints2["supplier_part_pricing_list"] = "company/price-break/";
  ApiEndpoints2["manufacturer_part_list"] = "company/part/manufacturer/";
  ApiEndpoints2["manufacturer_part_parameter_list"] = "company/part/manufacturer/parameter/";
  ApiEndpoints2["stock_location_list"] = "stock/location/";
  ApiEndpoints2["stock_location_type_list"] = "stock/location-type/";
  ApiEndpoints2["stock_location_tree"] = "stock/location/tree/";
  ApiEndpoints2["stock_item_list"] = "stock/";
  ApiEndpoints2["stock_tracking_list"] = "stock/track/";
  ApiEndpoints2["stock_test_result_list"] = "stock/test/";
  ApiEndpoints2["stock_transfer"] = "stock/transfer/";
  ApiEndpoints2["stock_remove"] = "stock/remove/";
  ApiEndpoints2["stock_return"] = "stock/return/";
  ApiEndpoints2["stock_add"] = "stock/add/";
  ApiEndpoints2["stock_count"] = "stock/count/";
  ApiEndpoints2["stock_change_status"] = "stock/change_status/";
  ApiEndpoints2["stock_merge"] = "stock/merge/";
  ApiEndpoints2["stock_assign"] = "stock/assign/";
  ApiEndpoints2["stock_status"] = "stock/status/";
  ApiEndpoints2["stock_install"] = "stock/:id/install/";
  ApiEndpoints2["stock_uninstall"] = "stock/:id/uninstall/";
  ApiEndpoints2["stock_serialize"] = "stock/:id/serialize/";
  ApiEndpoints2["stock_serial_info"] = "stock/:id/serial-numbers/";
  ApiEndpoints2["generate_batch_code"] = "generate/batch-code/";
  ApiEndpoints2["generate_serial_number"] = "generate/serial-number/";
  ApiEndpoints2["purchase_order_list"] = "order/po/";
  ApiEndpoints2["purchase_order_issue"] = "order/po/:id/issue/";
  ApiEndpoints2["purchase_order_hold"] = "order/po/:id/hold/";
  ApiEndpoints2["purchase_order_cancel"] = "order/po/:id/cancel/";
  ApiEndpoints2["purchase_order_complete"] = "order/po/:id/complete/";
  ApiEndpoints2["purchase_order_line_list"] = "order/po-line/";
  ApiEndpoints2["purchase_order_extra_line_list"] = "order/po-extra-line/";
  ApiEndpoints2["purchase_order_receive"] = "order/po/:id/receive/";
  ApiEndpoints2["sales_order_list"] = "order/so/";
  ApiEndpoints2["sales_order_issue"] = "order/so/:id/issue/";
  ApiEndpoints2["sales_order_hold"] = "order/so/:id/hold/";
  ApiEndpoints2["sales_order_cancel"] = "order/so/:id/cancel/";
  ApiEndpoints2["sales_order_ship"] = "order/so/:id/ship/";
  ApiEndpoints2["sales_order_complete"] = "order/so/:id/complete/";
  ApiEndpoints2["sales_order_allocate"] = "order/so/:id/allocate/";
  ApiEndpoints2["sales_order_allocate_serials"] = "order/so/:id/allocate-serials/";
  ApiEndpoints2["sales_order_line_list"] = "order/so-line/";
  ApiEndpoints2["sales_order_extra_line_list"] = "order/so-extra-line/";
  ApiEndpoints2["sales_order_allocation_list"] = "order/so-allocation/";
  ApiEndpoints2["sales_order_shipment_list"] = "order/so/shipment/";
  ApiEndpoints2["sales_order_shipment_complete"] = "order/so/shipment/:id/ship/";
  ApiEndpoints2["return_order_list"] = "order/ro/";
  ApiEndpoints2["return_order_issue"] = "order/ro/:id/issue/";
  ApiEndpoints2["return_order_hold"] = "order/ro/:id/hold/";
  ApiEndpoints2["return_order_cancel"] = "order/ro/:id/cancel/";
  ApiEndpoints2["return_order_complete"] = "order/ro/:id/complete/";
  ApiEndpoints2["return_order_receive"] = "order/ro/:id/receive/";
  ApiEndpoints2["return_order_line_list"] = "order/ro-line/";
  ApiEndpoints2["return_order_extra_line_list"] = "order/ro-extra-line/";
  ApiEndpoints2["label_list"] = "label/template/";
  ApiEndpoints2["label_print"] = "label/print/";
  ApiEndpoints2["report_list"] = "report/template/";
  ApiEndpoints2["report_print"] = "report/print/";
  ApiEndpoints2["report_snippet"] = "report/snippet/";
  ApiEndpoints2["report_asset"] = "report/asset/";
  ApiEndpoints2["plugin_list"] = "plugins/";
  ApiEndpoints2["plugin_setting_list"] = "plugins/:plugin/settings/";
  ApiEndpoints2["plugin_user_setting_list"] = "plugins/:plugin/user-settings/";
  ApiEndpoints2["plugin_registry_status"] = "plugins/status/";
  ApiEndpoints2["plugin_install"] = "plugins/install/";
  ApiEndpoints2["plugin_reload"] = "plugins/reload/";
  ApiEndpoints2["plugin_activate"] = "plugins/:key/activate/";
  ApiEndpoints2["plugin_uninstall"] = "plugins/:key/uninstall/";
  ApiEndpoints2["plugin_admin"] = "plugins/:key/admin/";
  ApiEndpoints2["plugin_ui_features_list"] = "plugins/ui/features/:feature_type/";
  ApiEndpoints2["plugin_locate_item"] = "locate/";
  ApiEndpoints2["machine_types_list"] = "machine/types/";
  ApiEndpoints2["machine_driver_list"] = "machine/drivers/";
  ApiEndpoints2["machine_registry_status"] = "machine/status/";
  ApiEndpoints2["machine_list"] = "machine/";
  ApiEndpoints2["machine_restart"] = "machine/:machine/restart/";
  ApiEndpoints2["machine_setting_list"] = "machine/:machine/settings/";
  ApiEndpoints2["machine_setting_detail"] = "machine/:machine/settings/:config_type/";
  ApiEndpoints2["attachment_list"] = "attachment/";
  ApiEndpoints2["error_report_list"] = "error-report/";
  ApiEndpoints2["project_code_list"] = "project-code/";
  ApiEndpoints2["custom_unit_list"] = "units/";
  ApiEndpoints2["notes_image_upload"] = "notes-image-upload/";
  ApiEndpoints2["email_list"] = "admin/email/";
  ApiEndpoints2["email_test"] = "admin/email/test/";
  ApiEndpoints2["config_list"] = "admin/config/";
  return ApiEndpoints2;
})(ApiEndpoints || {});
window["LinguiCore"].i18n;
function apiPrefix() {
  return "/api/";
}
function apiUrl(endpoint, pk, pathParams) {
  let _url = endpoint;
  if (!_url.startsWith("/")) {
    _url = apiPrefix() + _url;
  }
  if (_url && pk) {
    if (_url.indexOf(":id") >= 0) {
      _url = _url.replace(":id", `${pk}`);
    } else {
      _url += `${pk}/`;
    }
  }
  return _url;
}
window["LinguiCore"].i18n;
({
  part: {
    api_endpoint: ApiEndpoints.part_list
  },
  partparametertemplate: {
    api_endpoint: ApiEndpoints.part_parameter_template_list
  },
  parttesttemplate: {
    api_endpoint: ApiEndpoints.part_test_template_list
  },
  supplierpart: {
    api_endpoint: ApiEndpoints.supplier_part_list
  },
  manufacturerpart: {
    api_endpoint: ApiEndpoints.manufacturer_part_list
  },
  partcategory: {
    api_endpoint: ApiEndpoints.category_list
  },
  stockitem: {
    api_endpoint: ApiEndpoints.stock_item_list
  },
  stocklocation: {
    api_endpoint: ApiEndpoints.stock_location_list
  },
  stocklocationtype: {
    api_endpoint: ApiEndpoints.stock_location_type_list
  },
  stockhistory: {
    api_endpoint: ApiEndpoints.stock_tracking_list
  },
  build: {
    api_endpoint: ApiEndpoints.build_order_list
  },
  buildline: {
    api_endpoint: ApiEndpoints.build_line_list
  },
  builditem: {
    api_endpoint: ApiEndpoints.build_item_list
  },
  company: {
    api_endpoint: ApiEndpoints.company_list
  },
  projectcode: {
    api_endpoint: ApiEndpoints.project_code_list
  },
  purchaseorder: {
    api_endpoint: ApiEndpoints.purchase_order_list
  },
  purchaseorderlineitem: {
    api_endpoint: ApiEndpoints.purchase_order_line_list
  },
  salesorder: {
    api_endpoint: ApiEndpoints.sales_order_list
  },
  salesordershipment: {
    api_endpoint: ApiEndpoints.sales_order_shipment_list
  },
  returnorder: {
    api_endpoint: ApiEndpoints.return_order_list
  },
  returnorderlineitem: {
    api_endpoint: ApiEndpoints.return_order_line_list
  },
  address: {
    api_endpoint: ApiEndpoints.address_list
  },
  contact: {
    api_endpoint: ApiEndpoints.contact_list
  },
  owner: {
    api_endpoint: ApiEndpoints.owner_list
  },
  user: {
    api_endpoint: ApiEndpoints.user_list
  },
  group: {
    api_endpoint: ApiEndpoints.group_list
  },
  importsession: {
    api_endpoint: ApiEndpoints.import_session_list
  },
  labeltemplate: {
    api_endpoint: ApiEndpoints.label_list
  },
  reporttemplate: {
    api_endpoint: ApiEndpoints.report_list
  },
  pluginconfig: {
    api_endpoint: ApiEndpoints.plugin_list
  },
  contenttype: {
    api_endpoint: ApiEndpoints.content_type_list
  },
  selectionlist: {
    api_endpoint: ApiEndpoints.selectionlist_list
  },
  error: {
    api_endpoint: ApiEndpoints.error_report_list
  }
});
function cancelEvent(event) {
  var _a2;
  event == null ? void 0 : event.preventDefault();
  event == null ? void 0 : event.stopPropagation();
  (_a2 = event == null ? void 0 : event.nativeEvent) == null ? void 0 : _a2.stopImmediatePropagation();
}
function checkPluginVersion(context) {
  var _a2;
  const systemVersion = ((_a2 = context == null ? void 0 : context.version) == null ? void 0 : _a2.inventree) || "";
  if (INVENTREE_PLUGIN_VERSION != systemVersion) {
    console.info(`Plugin version mismatch! Expected version ${INVENTREE_PLUGIN_VERSION}, got ${systemVersion}`);
  }
}
function formatDecimal(value, options = {}) {
  const locale = options.locale || navigator.language || "en-US";
  if (value === null || value === void 0) {
    return value;
  }
  try {
    const formatter = new Intl.NumberFormat(locale, {
      style: "decimal",
      maximumFractionDigits: options.digits ?? 6,
      minimumFractionDigits: options.minDigits ?? 0
    });
    return formatter.format(value);
  } catch (e) {
    console.error("Error formatting decimal:", e);
    return value;
  }
}
function formatCurrencyValue(value, options = {}) {
  if (value == null || value == void 0) {
    return null;
  }
  value = Number.parseFloat(value.toString());
  if (Number.isNaN(value) || !Number.isFinite(value)) {
    return null;
  }
  value *= options.multiplier ?? 1;
  const locale = options.locale || navigator.language || "en-US";
  const minDigits = options.minDigits ?? 0;
  const maxDigits = options.digits ?? 6;
  try {
    const formatter = new Intl.NumberFormat(locale, {
      style: "currency",
      currency: options.currency || "USD",
      maximumFractionDigits: Math.max(minDigits, maxDigits),
      minimumFractionDigits: Math.min(minDigits, maxDigits)
    });
    return formatter.format(value);
  } catch (e) {
    console.error("Error formatting currency:", e);
    return value;
  }
}
var jsxRuntime$1 = { exports: {} };
var reactJsxRuntime_production$1 = {};
/**
 * @license React
 * react-jsx-runtime.production.js
 *
 * Copyright (c) Meta Platforms, Inc. and affiliates.
 *
 * This source code is licensed under the MIT license found in the
 * LICENSE file in the root directory of this source tree.
 */
var hasRequiredReactJsxRuntime_production$1;
function requireReactJsxRuntime_production$1() {
  if (hasRequiredReactJsxRuntime_production$1) return reactJsxRuntime_production$1;
  hasRequiredReactJsxRuntime_production$1 = 1;
  var REACT_ELEMENT_TYPE = Symbol.for("react.transitional.element"), REACT_FRAGMENT_TYPE = Symbol.for("react.fragment");
  function jsxProd(type, config, maybeKey) {
    var key = null;
    void 0 !== maybeKey && (key = "" + maybeKey);
    void 0 !== config.key && (key = "" + config.key);
    if ("key" in config) {
      maybeKey = {};
      for (var propName in config)
        "key" !== propName && (maybeKey[propName] = config[propName]);
    } else maybeKey = config;
    config = maybeKey.ref;
    return {
      $$typeof: REACT_ELEMENT_TYPE,
      type,
      key,
      ref: void 0 !== config ? config : null,
      props: maybeKey
    };
  }
  reactJsxRuntime_production$1.Fragment = REACT_FRAGMENT_TYPE;
  reactJsxRuntime_production$1.jsx = jsxProd;
  reactJsxRuntime_production$1.jsxs = jsxProd;
  return reactJsxRuntime_production$1;
}
var hasRequiredJsxRuntime$1;
function requireJsxRuntime$1() {
  if (hasRequiredJsxRuntime$1) return jsxRuntime$1.exports;
  hasRequiredJsxRuntime$1 = 1;
  {
    jsxRuntime$1.exports = requireReactJsxRuntime_production$1();
  }
  return jsxRuntime$1.exports;
}
var jsxRuntimeExports$1 = requireJsxRuntime$1();
function identifierString(value) {
  value = value || "-";
  return value.toLowerCase().replace(/[^a-z0-9]/g, "-");
}
const ActionIcon$1 = window["MantineCore"].ActionIcon;
const Group = window["MantineCore"].Group;
const Tooltip$1 = window["MantineCore"].Tooltip;
function ActionButton(props) {
  const hidden = props.hidden ?? false;
  return !hidden && /* @__PURE__ */ jsxRuntimeExports$1.jsx(Tooltip$1, { disabled: !props.tooltip && !props.text, label: props.tooltip ?? props.text, position: props.tooltipAlignment ?? "left", children: /* @__PURE__ */ jsxRuntimeExports$1.jsx(ActionIcon$1, { disabled: props.disabled, p: 17, radius: props.radius ?? "xs", color: props.color, size: props.size, "aria-label": `action-button-${identifierString(props.tooltip ?? props.text ?? "")}`, onClick: (event) => {
    props.onClick(event);
  }, variant: props.variant ?? "transparent", children: /* @__PURE__ */ jsxRuntimeExports$1.jsx(Group, { gap: "xs", wrap: "nowrap", children: props.icon }) }, `action-icon-${props.tooltip ?? props.text}`) }, `tooltip-${props.tooltip ?? props.text}`);
}
/**
 * @license @tabler/icons-react v3.34.1 - MIT
 *
 * This source code is licensed under the MIT license.
 * See the LICENSE file in the root directory of this source tree.
 */
var defaultAttributes$1 = {
  outline: {
    xmlns: "http://www.w3.org/2000/svg",
    width: 24,
    height: 24,
    viewBox: "0 0 24 24",
    fill: "none",
    stroke: "currentColor",
    strokeWidth: 2,
    strokeLinecap: "round",
    strokeLinejoin: "round"
  },
  filled: {
    xmlns: "http://www.w3.org/2000/svg",
    width: 24,
    height: 24,
    viewBox: "0 0 24 24",
    fill: "currentColor",
    stroke: "none"
  }
};
/**
 * @license @tabler/icons-react v3.34.1 - MIT
 *
 * This source code is licensed under the MIT license.
 * See the LICENSE file in the root directory of this source tree.
 */
const forwardRef$1 = window["React"].forwardRef;
const createElement$1 = window["React"].createElement;
const createReactComponent$1 = (type, iconName, iconNamePascal, iconNode) => {
  const Component = forwardRef$1(
    ({ color = "currentColor", size = 24, stroke = 2, title, className, children, ...rest }, ref) => createElement$1(
      "svg",
      {
        ref,
        ...defaultAttributes$1[type],
        width: size,
        height: size,
        className: [`tabler-icon`, `tabler-icon-${iconName}`, className].join(" "),
        ...{
          strokeWidth: stroke,
          stroke: color
        },
        ...rest
      },
      [
        title && createElement$1("title", { key: "svg-title" }, title),
        ...iconNode.map(([tag, attrs]) => createElement$1(tag, attrs)),
        ...Array.isArray(children) ? children : [children]
      ]
    )
  );
  Component.displayName = `${iconNamePascal}`;
  return Component;
};
/**
 * @license @tabler/icons-react v3.34.1 - MIT
 *
 * This source code is licensed under the MIT license.
 * See the LICENSE file in the root directory of this source tree.
 */
const __iconNode$a = [["path", { "d": "M12 5l0 14", "key": "svg-0" }], ["path", { "d": "M5 12l14 0", "key": "svg-1" }]];
const IconPlus = createReactComponent$1("outline", "plus", "Plus", __iconNode$a);
function AddItemButton(props) {
  return /* @__PURE__ */ jsxRuntimeExports$1.jsx(ActionButton, { ...props, color: "green", icon: /* @__PURE__ */ jsxRuntimeExports$1.jsx(IconPlus, {}) });
}
window["MantineCore"].ActionIcon;
window["MantineCore"].Menu;
window["MantineCore"].Tooltip;
window["MantineCore"].Progress;
window["MantineCore"].Stack;
window["MantineCore"].Text;
window["React"].useMemo;
window["LinguiCore"].i18n;
window["MantineCore"].Badge;
window["MantineCore"].Skeleton;
const useState$6 = window["React"].useState;
const useRef$5 = window["React"].useRef;
const useEffect$9 = window["React"].useEffect;
function useDebouncedValue(value, wait, options = { leading: false }) {
  const [_value, setValue] = useState$6(value);
  const mountedRef = useRef$5(false);
  const timeoutRef = useRef$5(null);
  const cooldownRef = useRef$5(false);
  const cancel = () => window.clearTimeout(timeoutRef.current);
  useEffect$9(() => {
    if (mountedRef.current) {
      if (!cooldownRef.current && options.leading) {
        cooldownRef.current = true;
        setValue(value);
      } else {
        cancel();
        timeoutRef.current = window.setTimeout(() => {
          cooldownRef.current = false;
          setValue(value);
        }, wait);
      }
    }
  }, [value, options.leading, wait]);
  useEffect$9(() => {
    mountedRef.current = true;
    return cancel;
  }, []);
  return [_value, cancel];
}
/**
 * @license @tabler/icons-react v3.34.1 - MIT
 *
 * This source code is licensed under the MIT license.
 * See the LICENSE file in the root directory of this source tree.
 */
const __iconNode$9 = [["path", { "d": "M10 10m-7 0a7 7 0 1 0 14 0a7 7 0 1 0 -14 0", "key": "svg-0" }], ["path", { "d": "M21 21l-6 -6", "key": "svg-1" }]];
const IconSearch = createReactComponent$1("outline", "search", "Search", __iconNode$9);
const _i18n$1 = window["LinguiCore"].i18n;
const CloseButton = window["MantineCore"].CloseButton;
const TextInput = window["MantineCore"].TextInput;
const useEffect$8 = window["React"].useEffect;
const useState$5 = window["React"].useState;
function SearchInput({
  disabled,
  debounce,
  placeholder,
  searchCallback
}) {
  const [value, setValue] = useState$5("");
  const [searchText] = useDebouncedValue(value, debounce ?? 500);
  useEffect$8(() => {
    searchCallback(searchText);
  }, [searchText]);
  return /* @__PURE__ */ jsxRuntimeExports$1.jsx(TextInput, { value, disabled, "aria-label": "table-search-input", leftSection: /* @__PURE__ */ jsxRuntimeExports$1.jsx(IconSearch, {}), placeholder: placeholder ?? _i18n$1._(
    /*i18n*/
    {
      id: "A1taO8"
    }
  ), onChange: (event) => setValue(event.target.value), rightSection: value.length > 0 ? /* @__PURE__ */ jsxRuntimeExports$1.jsx(CloseButton, { size: "xs", onClick: () => {
    setValue("");
    searchCallback("");
  } }) : null });
}
/**
 * @license @tabler/icons-react v3.34.1 - MIT
 *
 * This source code is licensed under the MIT license.
 * See the LICENSE file in the root directory of this source tree.
 */
const __iconNode$8 = [["path", { "d": "M5 12l14 0", "key": "svg-0" }], ["path", { "d": "M13 18l6 -6", "key": "svg-1" }], ["path", { "d": "M13 6l6 6", "key": "svg-2" }]];
createReactComponent$1("outline", "arrow-right", "ArrowRight", __iconNode$8);
/**
 * @license @tabler/icons-react v3.34.1 - MIT
 *
 * This source code is licensed under the MIT license.
 * See the LICENSE file in the root directory of this source tree.
 */
const __iconNode$7 = [["path", { "d": "M7 7m0 2.667a2.667 2.667 0 0 1 2.667 -2.667h8.666a2.667 2.667 0 0 1 2.667 2.667v8.666a2.667 2.667 0 0 1 -2.667 2.667h-8.666a2.667 2.667 0 0 1 -2.667 -2.667z", "key": "svg-0" }], ["path", { "d": "M4.012 16.737a2.005 2.005 0 0 1 -1.012 -1.737v-10c0 -1.1 .9 -2 2 -2h10c.75 0 1.158 .385 1.5 1", "key": "svg-1" }]];
const IconCopy = createReactComponent$1("outline", "copy", "Copy", __iconNode$7);
/**
 * @license @tabler/icons-react v3.34.1 - MIT
 *
 * This source code is licensed under the MIT license.
 * See the LICENSE file in the root directory of this source tree.
 */
const __iconNode$6 = [["path", { "d": "M7 7h-1a2 2 0 0 0 -2 2v9a2 2 0 0 0 2 2h9a2 2 0 0 0 2 -2v-1", "key": "svg-0" }], ["path", { "d": "M20.385 6.585a2.1 2.1 0 0 0 -2.97 -2.97l-8.415 8.385v3h3l8.385 -8.415z", "key": "svg-1" }], ["path", { "d": "M16 5l3 3", "key": "svg-2" }]];
const IconEdit = createReactComponent$1("outline", "edit", "Edit", __iconNode$6);
/**
 * @license @tabler/icons-react v3.34.1 - MIT
 *
 * This source code is licensed under the MIT license.
 * See the LICENSE file in the root directory of this source tree.
 */
const __iconNode$5 = [["path", { "d": "M4 7l16 0", "key": "svg-0" }], ["path", { "d": "M10 11l0 6", "key": "svg-1" }], ["path", { "d": "M14 11l0 6", "key": "svg-2" }], ["path", { "d": "M5 7l1 12a2 2 0 0 0 2 2h8a2 2 0 0 0 2 -2l1 -12", "key": "svg-3" }], ["path", { "d": "M9 7v-3a1 1 0 0 1 1 -1h4a1 1 0 0 1 1 1v3", "key": "svg-4" }]];
const IconTrash = createReactComponent$1("outline", "trash", "Trash", __iconNode$5);
/**
 * @license @tabler/icons-react v3.34.1 - MIT
 *
 * This source code is licensed under the MIT license.
 * See the LICENSE file in the root directory of this source tree.
 */
const __iconNode$4 = [["path", { "d": "M12 12m-9 0a9 9 0 1 0 18 0a9 9 0 1 0 -18 0", "key": "svg-0" }], ["path", { "d": "M10 10l4 4m0 -4l-4 4", "key": "svg-1" }]];
createReactComponent$1("outline", "circle-x", "CircleX", __iconNode$4);
/**
 * @license @tabler/icons-react v3.34.1 - MIT
 *
 * This source code is licensed under the MIT license.
 * See the LICENSE file in the root directory of this source tree.
 */
const __iconNode$3 = [["path", { "d": "M5 12m-1 0a1 1 0 1 0 2 0a1 1 0 1 0 -2 0", "key": "svg-0" }], ["path", { "d": "M12 12m-1 0a1 1 0 1 0 2 0a1 1 0 1 0 -2 0", "key": "svg-1" }], ["path", { "d": "M19 12m-1 0a1 1 0 1 0 2 0a1 1 0 1 0 -2 0", "key": "svg-2" }]];
const IconDots = createReactComponent$1("outline", "dots", "Dots", __iconNode$3);
const _i18n = window["LinguiCore"].i18n;
const ActionIcon = window["MantineCore"].ActionIcon;
const Menu = window["MantineCore"].Menu;
const Tooltip = window["MantineCore"].Tooltip;
const useMemo$3 = window["React"].useMemo;
const useState$4 = window["React"].useState;
function RowDuplicateAction(props) {
  return {
    ...props,
    title: _i18n._(
      /*i18n*/
      {
        id: "euc6Ns"
      }
    ),
    color: "green",
    icon: /* @__PURE__ */ jsxRuntimeExports$1.jsx(IconCopy, {})
  };
}
function RowEditAction(props) {
  return {
    ...props,
    title: _i18n._(
      /*i18n*/
      {
        id: "ePK91l"
      }
    ),
    color: "blue",
    icon: /* @__PURE__ */ jsxRuntimeExports$1.jsx(IconEdit, {})
  };
}
function RowDeleteAction(props) {
  return {
    ...props,
    title: _i18n._(
      /*i18n*/
      {
        id: "cnGeoo"
      }
    ),
    color: "red",
    icon: /* @__PURE__ */ jsxRuntimeExports$1.jsx(IconTrash, {})
  };
}
function RowActions({
  title,
  actions,
  disabled = false,
  index
}) {
  function openMenu(event) {
    cancelEvent(event);
    setOpened(!opened);
  }
  const [opened, setOpened] = useState$4(false);
  const visibleActions = useMemo$3(() => {
    return actions.filter((action) => !action.hidden);
  }, [actions]);
  function RowActionIcon(action) {
    return /* @__PURE__ */ jsxRuntimeExports$1.jsx(Tooltip, { withinPortal: true, label: action.tooltip ?? action.title, position: "left", children: /* @__PURE__ */ jsxRuntimeExports$1.jsx(Menu.Item, { color: action.color, leftSection: action.icon, onClick: (event) => {
      var _a2;
      cancelEvent(event);
      (_a2 = action.onClick) == null ? void 0 : _a2.call(action, event);
      setOpened(false);
    }, disabled: action.disabled || false, children: action.title }) }, action.title);
  }
  return visibleActions.length > 0 && /* @__PURE__ */ jsxRuntimeExports$1.jsxs(Menu, { withinPortal: true, disabled, position: "bottom-end", opened, onChange: setOpened, children: [
    /* @__PURE__ */ jsxRuntimeExports$1.jsx(Menu.Target, { children: /* @__PURE__ */ jsxRuntimeExports$1.jsx(Tooltip, { withinPortal: true, label: title || _i18n._(
      /*i18n*/
      {
        id: "7L01XJ"
      }
    ), children: /* @__PURE__ */ jsxRuntimeExports$1.jsx(ActionIcon, { "aria-label": `row-action-menu-${index ?? ""}`, onClick: openMenu, disabled, variant: "subtle", color: "gray", children: /* @__PURE__ */ jsxRuntimeExports$1.jsx(IconDots, {}) }, `row-action-menu-${index ?? ""}`) }) }),
    /* @__PURE__ */ jsxRuntimeExports$1.jsx(Menu.Dropdown, { children: visibleActions.map((action) => /* @__PURE__ */ jsxRuntimeExports$1.jsx(RowActionIcon, { ...action }, action.title)) })
  ] });
}
/**
 * @license @tabler/icons-react v3.34.1 - MIT
 *
 * This source code is licensed under the MIT license.
 * See the LICENSE file in the root directory of this source tree.
 */
var defaultAttributes = {
  outline: {
    xmlns: "http://www.w3.org/2000/svg",
    width: 24,
    height: 24,
    viewBox: "0 0 24 24",
    fill: "none",
    stroke: "currentColor",
    strokeWidth: 2,
    strokeLinecap: "round",
    strokeLinejoin: "round"
  },
  filled: {
    xmlns: "http://www.w3.org/2000/svg",
    width: 24,
    height: 24,
    viewBox: "0 0 24 24",
    fill: "currentColor",
    stroke: "none"
  }
};
/**
 * @license @tabler/icons-react v3.34.1 - MIT
 *
 * This source code is licensed under the MIT license.
 * See the LICENSE file in the root directory of this source tree.
 */
const forwardRef = window["React"].forwardRef;
const createElement = window["React"].createElement;
const createReactComponent = (type, iconName, iconNamePascal, iconNode) => {
  const Component = forwardRef(
    ({ color = "currentColor", size = 24, stroke = 2, title, className, children, ...rest }, ref) => createElement(
      "svg",
      {
        ref,
        ...defaultAttributes[type],
        width: size,
        height: size,
        className: [`tabler-icon`, `tabler-icon-${iconName}`, className].join(" "),
        ...{
          strokeWidth: stroke,
          stroke: color
        },
        ...rest
      },
      [
        title && createElement("title", { key: "svg-title" }, title),
        ...iconNode.map(([tag, attrs]) => createElement(tag, attrs)),
        ...Array.isArray(children) ? children : [children]
      ]
    )
  );
  Component.displayName = `${iconNamePascal}`;
  return Component;
};
/**
 * @license @tabler/icons-react v3.34.1 - MIT
 *
 * This source code is licensed under the MIT license.
 * See the LICENSE file in the root directory of this source tree.
 */
const __iconNode$2 = [["path", { "d": "M12 12m-9 0a9 9 0 1 0 18 0a9 9 0 1 0 -18 0", "key": "svg-0" }], ["path", { "d": "M12 9v4", "key": "svg-1" }], ["path", { "d": "M12 16v.01", "key": "svg-2" }]];
const IconExclamationCircle = createReactComponent("outline", "exclamation-circle", "ExclamationCircle", __iconNode$2);
/**
 * @license @tabler/icons-react v3.34.1 - MIT
 *
 * This source code is licensed under the MIT license.
 * See the LICENSE file in the root directory of this source tree.
 */
const __iconNode$1 = [["path", { "d": "M3 12a9 9 0 1 0 18 0a9 9 0 0 0 -18 0", "key": "svg-0" }], ["path", { "d": "M12 9h.01", "key": "svg-1" }], ["path", { "d": "M11 12h1v4h1", "key": "svg-2" }]];
const IconInfoCircle = createReactComponent("outline", "info-circle", "InfoCircle", __iconNode$1);
/**
 * @license @tabler/icons-react v3.34.1 - MIT
 *
 * This source code is licensed under the MIT license.
 * See the LICENSE file in the root directory of this source tree.
 */
const __iconNode = [["path", { "d": "M20 11a8.1 8.1 0 0 0 -15.5 -2m-.5 -4v4h4", "key": "svg-0" }], ["path", { "d": "M4 13a8.1 8.1 0 0 0 15.5 2m.5 4v-4h-4", "key": "svg-1" }]];
const IconRefresh = createReactComponent("outline", "refresh", "Refresh", __iconNode);
var Subscribable = class {
  constructor() {
    this.listeners = /* @__PURE__ */ new Set();
    this.subscribe = this.subscribe.bind(this);
  }
  subscribe(listener) {
    this.listeners.add(listener);
    this.onSubscribe();
    return () => {
      this.listeners.delete(listener);
      this.onUnsubscribe();
    };
  }
  hasListeners() {
    return this.listeners.size > 0;
  }
  onSubscribe() {
  }
  onUnsubscribe() {
  }
};
var isServer = typeof window === "undefined" || "Deno" in globalThis;
function noop() {
}
function isValidTimeout(value) {
  return typeof value === "number" && value >= 0 && value !== Infinity;
}
function timeUntilStale(updatedAt, staleTime) {
  return Math.max(updatedAt + (staleTime || 0) - Date.now(), 0);
}
function resolveStaleTime(staleTime, query) {
  return typeof staleTime === "function" ? staleTime(query) : staleTime;
}
function resolveEnabled(enabled, query) {
  return typeof enabled === "function" ? enabled(query) : enabled;
}
var hasOwn = Object.prototype.hasOwnProperty;
function replaceEqualDeep(a, b) {
  if (a === b) {
    return a;
  }
  const array = isPlainArray(a) && isPlainArray(b);
  if (!array && !(isPlainObject(a) && isPlainObject(b))) return b;
  const aItems = array ? a : Object.keys(a);
  const aSize = aItems.length;
  const bItems = array ? b : Object.keys(b);
  const bSize = bItems.length;
  const copy = array ? new Array(bSize) : {};
  let equalItems = 0;
  for (let i = 0; i < bSize; i++) {
    const key = array ? i : bItems[i];
    const aItem = a[key];
    const bItem = b[key];
    if (aItem === bItem) {
      copy[key] = aItem;
      if (array ? i < aSize : hasOwn.call(a, key)) equalItems++;
      continue;
    }
    if (aItem === null || bItem === null || typeof aItem !== "object" || typeof bItem !== "object") {
      copy[key] = bItem;
      continue;
    }
    const v2 = replaceEqualDeep(aItem, bItem);
    copy[key] = v2;
    if (v2 === aItem) equalItems++;
  }
  return aSize === bSize && equalItems === aSize ? a : copy;
}
function shallowEqualObjects(a, b) {
  if (!b || Object.keys(a).length !== Object.keys(b).length) {
    return false;
  }
  for (const key in a) {
    if (a[key] !== b[key]) {
      return false;
    }
  }
  return true;
}
function isPlainArray(value) {
  return Array.isArray(value) && value.length === Object.keys(value).length;
}
function isPlainObject(o) {
  if (!hasObjectPrototype(o)) {
    return false;
  }
  const ctor = o.constructor;
  if (ctor === void 0) {
    return true;
  }
  const prot = ctor.prototype;
  if (!hasObjectPrototype(prot)) {
    return false;
  }
  if (!prot.hasOwnProperty("isPrototypeOf")) {
    return false;
  }
  if (Object.getPrototypeOf(o) !== Object.prototype) {
    return false;
  }
  return true;
}
function hasObjectPrototype(o) {
  return Object.prototype.toString.call(o) === "[object Object]";
}
function replaceData(prevData, data, options) {
  if (typeof options.structuralSharing === "function") {
    return options.structuralSharing(prevData, data);
  } else if (options.structuralSharing !== false) {
    return replaceEqualDeep(prevData, data);
  }
  return data;
}
function shouldThrowError(throwOnError, params) {
  if (typeof throwOnError === "function") {
    return throwOnError(...params);
  }
  return !!throwOnError;
}
var FocusManager = (_a = class extends Subscribable {
  constructor() {
    super();
    __privateAdd(this, _focused);
    __privateAdd(this, _cleanup);
    __privateAdd(this, _setup);
    __privateSet(this, _setup, (onFocus) => {
      if (!isServer && window.addEventListener) {
        const listener = () => onFocus();
        window.addEventListener("visibilitychange", listener, false);
        return () => {
          window.removeEventListener("visibilitychange", listener);
        };
      }
      return;
    });
  }
  onSubscribe() {
    if (!__privateGet(this, _cleanup)) {
      this.setEventListener(__privateGet(this, _setup));
    }
  }
  onUnsubscribe() {
    var _a2;
    if (!this.hasListeners()) {
      (_a2 = __privateGet(this, _cleanup)) == null ? void 0 : _a2.call(this);
      __privateSet(this, _cleanup, void 0);
    }
  }
  setEventListener(setup) {
    var _a2;
    __privateSet(this, _setup, setup);
    (_a2 = __privateGet(this, _cleanup)) == null ? void 0 : _a2.call(this);
    __privateSet(this, _cleanup, setup((focused) => {
      if (typeof focused === "boolean") {
        this.setFocused(focused);
      } else {
        this.onFocus();
      }
    }));
  }
  setFocused(focused) {
    const changed = __privateGet(this, _focused) !== focused;
    if (changed) {
      __privateSet(this, _focused, focused);
      this.onFocus();
    }
  }
  onFocus() {
    const isFocused = this.isFocused();
    this.listeners.forEach((listener) => {
      listener(isFocused);
    });
  }
  isFocused() {
    var _a2;
    if (typeof __privateGet(this, _focused) === "boolean") {
      return __privateGet(this, _focused);
    }
    return ((_a2 = globalThis.document) == null ? void 0 : _a2.visibilityState) !== "hidden";
  }
}, _focused = new WeakMap(), _cleanup = new WeakMap(), _setup = new WeakMap(), _a);
var focusManager = new FocusManager();
var OnlineManager = (_b = class extends Subscribable {
  constructor() {
    super();
    __privateAdd(this, _online, true);
    __privateAdd(this, _cleanup2);
    __privateAdd(this, _setup2);
    __privateSet(this, _setup2, (onOnline) => {
      if (!isServer && window.addEventListener) {
        const onlineListener = () => onOnline(true);
        const offlineListener = () => onOnline(false);
        window.addEventListener("online", onlineListener, false);
        window.addEventListener("offline", offlineListener, false);
        return () => {
          window.removeEventListener("online", onlineListener);
          window.removeEventListener("offline", offlineListener);
        };
      }
      return;
    });
  }
  onSubscribe() {
    if (!__privateGet(this, _cleanup2)) {
      this.setEventListener(__privateGet(this, _setup2));
    }
  }
  onUnsubscribe() {
    var _a2;
    if (!this.hasListeners()) {
      (_a2 = __privateGet(this, _cleanup2)) == null ? void 0 : _a2.call(this);
      __privateSet(this, _cleanup2, void 0);
    }
  }
  setEventListener(setup) {
    var _a2;
    __privateSet(this, _setup2, setup);
    (_a2 = __privateGet(this, _cleanup2)) == null ? void 0 : _a2.call(this);
    __privateSet(this, _cleanup2, setup(this.setOnline.bind(this)));
  }
  setOnline(online) {
    const changed = __privateGet(this, _online) !== online;
    if (changed) {
      __privateSet(this, _online, online);
      this.listeners.forEach((listener) => {
        listener(online);
      });
    }
  }
  isOnline() {
    return __privateGet(this, _online);
  }
}, _online = new WeakMap(), _cleanup2 = new WeakMap(), _setup2 = new WeakMap(), _b);
var onlineManager = new OnlineManager();
function pendingThenable() {
  let resolve;
  let reject;
  const thenable = new Promise((_resolve, _reject) => {
    resolve = _resolve;
    reject = _reject;
  });
  thenable.status = "pending";
  thenable.catch(() => {
  });
  function finalize(data) {
    Object.assign(thenable, data);
    delete thenable.resolve;
    delete thenable.reject;
  }
  thenable.resolve = (value) => {
    finalize({
      status: "fulfilled",
      value
    });
    resolve(value);
  };
  thenable.reject = (reason) => {
    finalize({
      status: "rejected",
      reason
    });
    reject(reason);
  };
  return thenable;
}
function canFetch(networkMode) {
  return (networkMode ?? "online") === "online" ? onlineManager.isOnline() : true;
}
var defaultScheduler = (cb) => setTimeout(cb, 0);
function createNotifyManager() {
  let queue = [];
  let transactions = 0;
  let notifyFn = (callback) => {
    callback();
  };
  let batchNotifyFn = (callback) => {
    callback();
  };
  let scheduleFn = defaultScheduler;
  const schedule = (callback) => {
    if (transactions) {
      queue.push(callback);
    } else {
      scheduleFn(() => {
        notifyFn(callback);
      });
    }
  };
  const flush = () => {
    const originalQueue = queue;
    queue = [];
    if (originalQueue.length) {
      scheduleFn(() => {
        batchNotifyFn(() => {
          originalQueue.forEach((callback) => {
            notifyFn(callback);
          });
        });
      });
    }
  };
  return {
    batch: (callback) => {
      let result;
      transactions++;
      try {
        result = callback();
      } finally {
        transactions--;
        if (!transactions) {
          flush();
        }
      }
      return result;
    },
    /**
     * All calls to the wrapped function will be batched.
     */
    batchCalls: (callback) => {
      return (...args) => {
        schedule(() => {
          callback(...args);
        });
      };
    },
    schedule,
    /**
     * Use this method to set a custom notify function.
     * This can be used to for example wrap notifications with `React.act` while running tests.
     */
    setNotifyFunction: (fn) => {
      notifyFn = fn;
    },
    /**
     * Use this method to set a custom function to batch notifications together into a single tick.
     * By default React Query will use the batch function provided by ReactDOM or React Native.
     */
    setBatchNotifyFunction: (fn) => {
      batchNotifyFn = fn;
    },
    setScheduler: (fn) => {
      scheduleFn = fn;
    }
  };
}
var notifyManager = createNotifyManager();
function fetchState(data, options) {
  return {
    fetchFailureCount: 0,
    fetchFailureReason: null,
    fetchStatus: canFetch(options.networkMode) ? "fetching" : "paused",
    ...data === void 0 && {
      error: null,
      status: "pending"
    }
  };
}
var QueryObserver = (_c = class extends Subscribable {
  constructor(client, options) {
    super();
    __privateAdd(this, _QueryObserver_instances);
    __privateAdd(this, _client);
    __privateAdd(this, _currentQuery);
    __privateAdd(this, _currentQueryInitialState);
    __privateAdd(this, _currentResult);
    __privateAdd(this, _currentResultState);
    __privateAdd(this, _currentResultOptions);
    __privateAdd(this, _currentThenable);
    __privateAdd(this, _selectError);
    __privateAdd(this, _selectFn);
    __privateAdd(this, _selectResult);
    // This property keeps track of the last query with defined data.
    // It will be used to pass the previous data and query to the placeholder function between renders.
    __privateAdd(this, _lastQueryWithDefinedData);
    __privateAdd(this, _staleTimeoutId);
    __privateAdd(this, _refetchIntervalId);
    __privateAdd(this, _currentRefetchInterval);
    __privateAdd(this, _trackedProps, /* @__PURE__ */ new Set());
    this.options = options;
    __privateSet(this, _client, client);
    __privateSet(this, _selectError, null);
    __privateSet(this, _currentThenable, pendingThenable());
    this.bindMethods();
    this.setOptions(options);
  }
  bindMethods() {
    this.refetch = this.refetch.bind(this);
  }
  onSubscribe() {
    if (this.listeners.size === 1) {
      __privateGet(this, _currentQuery).addObserver(this);
      if (shouldFetchOnMount(__privateGet(this, _currentQuery), this.options)) {
        __privateMethod(this, _QueryObserver_instances, executeFetch_fn).call(this);
      } else {
        this.updateResult();
      }
      __privateMethod(this, _QueryObserver_instances, updateTimers_fn).call(this);
    }
  }
  onUnsubscribe() {
    if (!this.hasListeners()) {
      this.destroy();
    }
  }
  shouldFetchOnReconnect() {
    return shouldFetchOn(
      __privateGet(this, _currentQuery),
      this.options,
      this.options.refetchOnReconnect
    );
  }
  shouldFetchOnWindowFocus() {
    return shouldFetchOn(
      __privateGet(this, _currentQuery),
      this.options,
      this.options.refetchOnWindowFocus
    );
  }
  destroy() {
    this.listeners = /* @__PURE__ */ new Set();
    __privateMethod(this, _QueryObserver_instances, clearStaleTimeout_fn).call(this);
    __privateMethod(this, _QueryObserver_instances, clearRefetchInterval_fn).call(this);
    __privateGet(this, _currentQuery).removeObserver(this);
  }
  setOptions(options) {
    const prevOptions = this.options;
    const prevQuery = __privateGet(this, _currentQuery);
    this.options = __privateGet(this, _client).defaultQueryOptions(options);
    if (this.options.enabled !== void 0 && typeof this.options.enabled !== "boolean" && typeof this.options.enabled !== "function" && typeof resolveEnabled(this.options.enabled, __privateGet(this, _currentQuery)) !== "boolean") {
      throw new Error(
        "Expected enabled to be a boolean or a callback that returns a boolean"
      );
    }
    __privateMethod(this, _QueryObserver_instances, updateQuery_fn).call(this);
    __privateGet(this, _currentQuery).setOptions(this.options);
    if (prevOptions._defaulted && !shallowEqualObjects(this.options, prevOptions)) {
      __privateGet(this, _client).getQueryCache().notify({
        type: "observerOptionsUpdated",
        query: __privateGet(this, _currentQuery),
        observer: this
      });
    }
    const mounted = this.hasListeners();
    if (mounted && shouldFetchOptionally(
      __privateGet(this, _currentQuery),
      prevQuery,
      this.options,
      prevOptions
    )) {
      __privateMethod(this, _QueryObserver_instances, executeFetch_fn).call(this);
    }
    this.updateResult();
    if (mounted && (__privateGet(this, _currentQuery) !== prevQuery || resolveEnabled(this.options.enabled, __privateGet(this, _currentQuery)) !== resolveEnabled(prevOptions.enabled, __privateGet(this, _currentQuery)) || resolveStaleTime(this.options.staleTime, __privateGet(this, _currentQuery)) !== resolveStaleTime(prevOptions.staleTime, __privateGet(this, _currentQuery)))) {
      __privateMethod(this, _QueryObserver_instances, updateStaleTimeout_fn).call(this);
    }
    const nextRefetchInterval = __privateMethod(this, _QueryObserver_instances, computeRefetchInterval_fn).call(this);
    if (mounted && (__privateGet(this, _currentQuery) !== prevQuery || resolveEnabled(this.options.enabled, __privateGet(this, _currentQuery)) !== resolveEnabled(prevOptions.enabled, __privateGet(this, _currentQuery)) || nextRefetchInterval !== __privateGet(this, _currentRefetchInterval))) {
      __privateMethod(this, _QueryObserver_instances, updateRefetchInterval_fn).call(this, nextRefetchInterval);
    }
  }
  getOptimisticResult(options) {
    const query = __privateGet(this, _client).getQueryCache().build(__privateGet(this, _client), options);
    const result = this.createResult(query, options);
    if (shouldAssignObserverCurrentProperties(this, result)) {
      __privateSet(this, _currentResult, result);
      __privateSet(this, _currentResultOptions, this.options);
      __privateSet(this, _currentResultState, __privateGet(this, _currentQuery).state);
    }
    return result;
  }
  getCurrentResult() {
    return __privateGet(this, _currentResult);
  }
  trackResult(result, onPropTracked) {
    return new Proxy(result, {
      get: (target, key) => {
        this.trackProp(key);
        onPropTracked == null ? void 0 : onPropTracked(key);
        if (key === "promise" && !this.options.experimental_prefetchInRender && __privateGet(this, _currentThenable).status === "pending") {
          __privateGet(this, _currentThenable).reject(
            new Error(
              "experimental_prefetchInRender feature flag is not enabled"
            )
          );
        }
        return Reflect.get(target, key);
      }
    });
  }
  trackProp(key) {
    __privateGet(this, _trackedProps).add(key);
  }
  getCurrentQuery() {
    return __privateGet(this, _currentQuery);
  }
  refetch({ ...options } = {}) {
    return this.fetch({
      ...options
    });
  }
  fetchOptimistic(options) {
    const defaultedOptions = __privateGet(this, _client).defaultQueryOptions(options);
    const query = __privateGet(this, _client).getQueryCache().build(__privateGet(this, _client), defaultedOptions);
    return query.fetch().then(() => this.createResult(query, defaultedOptions));
  }
  fetch(fetchOptions) {
    return __privateMethod(this, _QueryObserver_instances, executeFetch_fn).call(this, {
      ...fetchOptions,
      cancelRefetch: fetchOptions.cancelRefetch ?? true
    }).then(() => {
      this.updateResult();
      return __privateGet(this, _currentResult);
    });
  }
  createResult(query, options) {
    var _a2;
    const prevQuery = __privateGet(this, _currentQuery);
    const prevOptions = this.options;
    const prevResult = __privateGet(this, _currentResult);
    const prevResultState = __privateGet(this, _currentResultState);
    const prevResultOptions = __privateGet(this, _currentResultOptions);
    const queryChange = query !== prevQuery;
    const queryInitialState = queryChange ? query.state : __privateGet(this, _currentQueryInitialState);
    const { state } = query;
    let newState = { ...state };
    let isPlaceholderData = false;
    let data;
    if (options._optimisticResults) {
      const mounted = this.hasListeners();
      const fetchOnMount = !mounted && shouldFetchOnMount(query, options);
      const fetchOptionally = mounted && shouldFetchOptionally(query, prevQuery, options, prevOptions);
      if (fetchOnMount || fetchOptionally) {
        newState = {
          ...newState,
          ...fetchState(state.data, query.options)
        };
      }
      if (options._optimisticResults === "isRestoring") {
        newState.fetchStatus = "idle";
      }
    }
    let { error, errorUpdatedAt, status } = newState;
    data = newState.data;
    let skipSelect = false;
    if (options.placeholderData !== void 0 && data === void 0 && status === "pending") {
      let placeholderData;
      if ((prevResult == null ? void 0 : prevResult.isPlaceholderData) && options.placeholderData === (prevResultOptions == null ? void 0 : prevResultOptions.placeholderData)) {
        placeholderData = prevResult.data;
        skipSelect = true;
      } else {
        placeholderData = typeof options.placeholderData === "function" ? options.placeholderData(
          (_a2 = __privateGet(this, _lastQueryWithDefinedData)) == null ? void 0 : _a2.state.data,
          __privateGet(this, _lastQueryWithDefinedData)
        ) : options.placeholderData;
      }
      if (placeholderData !== void 0) {
        status = "success";
        data = replaceData(
          prevResult == null ? void 0 : prevResult.data,
          placeholderData,
          options
        );
        isPlaceholderData = true;
      }
    }
    if (options.select && data !== void 0 && !skipSelect) {
      if (prevResult && data === (prevResultState == null ? void 0 : prevResultState.data) && options.select === __privateGet(this, _selectFn)) {
        data = __privateGet(this, _selectResult);
      } else {
        try {
          __privateSet(this, _selectFn, options.select);
          data = options.select(data);
          data = replaceData(prevResult == null ? void 0 : prevResult.data, data, options);
          __privateSet(this, _selectResult, data);
          __privateSet(this, _selectError, null);
        } catch (selectError) {
          __privateSet(this, _selectError, selectError);
        }
      }
    }
    if (__privateGet(this, _selectError)) {
      error = __privateGet(this, _selectError);
      data = __privateGet(this, _selectResult);
      errorUpdatedAt = Date.now();
      status = "error";
    }
    const isFetching = newState.fetchStatus === "fetching";
    const isPending = status === "pending";
    const isError = status === "error";
    const isLoading = isPending && isFetching;
    const hasData = data !== void 0;
    const result = {
      status,
      fetchStatus: newState.fetchStatus,
      isPending,
      isSuccess: status === "success",
      isError,
      isInitialLoading: isLoading,
      isLoading,
      data,
      dataUpdatedAt: newState.dataUpdatedAt,
      error,
      errorUpdatedAt,
      failureCount: newState.fetchFailureCount,
      failureReason: newState.fetchFailureReason,
      errorUpdateCount: newState.errorUpdateCount,
      isFetched: newState.dataUpdateCount > 0 || newState.errorUpdateCount > 0,
      isFetchedAfterMount: newState.dataUpdateCount > queryInitialState.dataUpdateCount || newState.errorUpdateCount > queryInitialState.errorUpdateCount,
      isFetching,
      isRefetching: isFetching && !isPending,
      isLoadingError: isError && !hasData,
      isPaused: newState.fetchStatus === "paused",
      isPlaceholderData,
      isRefetchError: isError && hasData,
      isStale: isStale(query, options),
      refetch: this.refetch,
      promise: __privateGet(this, _currentThenable),
      isEnabled: resolveEnabled(options.enabled, query) !== false
    };
    const nextResult = result;
    if (this.options.experimental_prefetchInRender) {
      const finalizeThenableIfPossible = (thenable) => {
        if (nextResult.status === "error") {
          thenable.reject(nextResult.error);
        } else if (nextResult.data !== void 0) {
          thenable.resolve(nextResult.data);
        }
      };
      const recreateThenable = () => {
        const pending = __privateSet(this, _currentThenable, nextResult.promise = pendingThenable());
        finalizeThenableIfPossible(pending);
      };
      const prevThenable = __privateGet(this, _currentThenable);
      switch (prevThenable.status) {
        case "pending":
          if (query.queryHash === prevQuery.queryHash) {
            finalizeThenableIfPossible(prevThenable);
          }
          break;
        case "fulfilled":
          if (nextResult.status === "error" || nextResult.data !== prevThenable.value) {
            recreateThenable();
          }
          break;
        case "rejected":
          if (nextResult.status !== "error" || nextResult.error !== prevThenable.reason) {
            recreateThenable();
          }
          break;
      }
    }
    return nextResult;
  }
  updateResult() {
    const prevResult = __privateGet(this, _currentResult);
    const nextResult = this.createResult(__privateGet(this, _currentQuery), this.options);
    __privateSet(this, _currentResultState, __privateGet(this, _currentQuery).state);
    __privateSet(this, _currentResultOptions, this.options);
    if (__privateGet(this, _currentResultState).data !== void 0) {
      __privateSet(this, _lastQueryWithDefinedData, __privateGet(this, _currentQuery));
    }
    if (shallowEqualObjects(nextResult, prevResult)) {
      return;
    }
    __privateSet(this, _currentResult, nextResult);
    const shouldNotifyListeners = () => {
      if (!prevResult) {
        return true;
      }
      const { notifyOnChangeProps } = this.options;
      const notifyOnChangePropsValue = typeof notifyOnChangeProps === "function" ? notifyOnChangeProps() : notifyOnChangeProps;
      if (notifyOnChangePropsValue === "all" || !notifyOnChangePropsValue && !__privateGet(this, _trackedProps).size) {
        return true;
      }
      const includedProps = new Set(
        notifyOnChangePropsValue ?? __privateGet(this, _trackedProps)
      );
      if (this.options.throwOnError) {
        includedProps.add("error");
      }
      return Object.keys(__privateGet(this, _currentResult)).some((key) => {
        const typedKey = key;
        const changed = __privateGet(this, _currentResult)[typedKey] !== prevResult[typedKey];
        return changed && includedProps.has(typedKey);
      });
    };
    __privateMethod(this, _QueryObserver_instances, notify_fn).call(this, { listeners: shouldNotifyListeners() });
  }
  onQueryUpdate() {
    this.updateResult();
    if (this.hasListeners()) {
      __privateMethod(this, _QueryObserver_instances, updateTimers_fn).call(this);
    }
  }
}, _client = new WeakMap(), _currentQuery = new WeakMap(), _currentQueryInitialState = new WeakMap(), _currentResult = new WeakMap(), _currentResultState = new WeakMap(), _currentResultOptions = new WeakMap(), _currentThenable = new WeakMap(), _selectError = new WeakMap(), _selectFn = new WeakMap(), _selectResult = new WeakMap(), _lastQueryWithDefinedData = new WeakMap(), _staleTimeoutId = new WeakMap(), _refetchIntervalId = new WeakMap(), _currentRefetchInterval = new WeakMap(), _trackedProps = new WeakMap(), _QueryObserver_instances = new WeakSet(), executeFetch_fn = function(fetchOptions) {
  __privateMethod(this, _QueryObserver_instances, updateQuery_fn).call(this);
  let promise = __privateGet(this, _currentQuery).fetch(
    this.options,
    fetchOptions
  );
  if (!(fetchOptions == null ? void 0 : fetchOptions.throwOnError)) {
    promise = promise.catch(noop);
  }
  return promise;
}, updateStaleTimeout_fn = function() {
  __privateMethod(this, _QueryObserver_instances, clearStaleTimeout_fn).call(this);
  const staleTime = resolveStaleTime(
    this.options.staleTime,
    __privateGet(this, _currentQuery)
  );
  if (isServer || __privateGet(this, _currentResult).isStale || !isValidTimeout(staleTime)) {
    return;
  }
  const time = timeUntilStale(__privateGet(this, _currentResult).dataUpdatedAt, staleTime);
  const timeout = time + 1;
  __privateSet(this, _staleTimeoutId, setTimeout(() => {
    if (!__privateGet(this, _currentResult).isStale) {
      this.updateResult();
    }
  }, timeout));
}, computeRefetchInterval_fn = function() {
  return (typeof this.options.refetchInterval === "function" ? this.options.refetchInterval(__privateGet(this, _currentQuery)) : this.options.refetchInterval) ?? false;
}, updateRefetchInterval_fn = function(nextInterval) {
  __privateMethod(this, _QueryObserver_instances, clearRefetchInterval_fn).call(this);
  __privateSet(this, _currentRefetchInterval, nextInterval);
  if (isServer || resolveEnabled(this.options.enabled, __privateGet(this, _currentQuery)) === false || !isValidTimeout(__privateGet(this, _currentRefetchInterval)) || __privateGet(this, _currentRefetchInterval) === 0) {
    return;
  }
  __privateSet(this, _refetchIntervalId, setInterval(() => {
    if (this.options.refetchIntervalInBackground || focusManager.isFocused()) {
      __privateMethod(this, _QueryObserver_instances, executeFetch_fn).call(this);
    }
  }, __privateGet(this, _currentRefetchInterval)));
}, updateTimers_fn = function() {
  __privateMethod(this, _QueryObserver_instances, updateStaleTimeout_fn).call(this);
  __privateMethod(this, _QueryObserver_instances, updateRefetchInterval_fn).call(this, __privateMethod(this, _QueryObserver_instances, computeRefetchInterval_fn).call(this));
}, clearStaleTimeout_fn = function() {
  if (__privateGet(this, _staleTimeoutId)) {
    clearTimeout(__privateGet(this, _staleTimeoutId));
    __privateSet(this, _staleTimeoutId, void 0);
  }
}, clearRefetchInterval_fn = function() {
  if (__privateGet(this, _refetchIntervalId)) {
    clearInterval(__privateGet(this, _refetchIntervalId));
    __privateSet(this, _refetchIntervalId, void 0);
  }
}, updateQuery_fn = function() {
  const query = __privateGet(this, _client).getQueryCache().build(__privateGet(this, _client), this.options);
  if (query === __privateGet(this, _currentQuery)) {
    return;
  }
  const prevQuery = __privateGet(this, _currentQuery);
  __privateSet(this, _currentQuery, query);
  __privateSet(this, _currentQueryInitialState, query.state);
  if (this.hasListeners()) {
    prevQuery == null ? void 0 : prevQuery.removeObserver(this);
    query.addObserver(this);
  }
}, notify_fn = function(notifyOptions) {
  notifyManager.batch(() => {
    if (notifyOptions.listeners) {
      this.listeners.forEach((listener) => {
        listener(__privateGet(this, _currentResult));
      });
    }
    __privateGet(this, _client).getQueryCache().notify({
      query: __privateGet(this, _currentQuery),
      type: "observerResultsUpdated"
    });
  });
}, _c);
function shouldLoadOnMount(query, options) {
  return resolveEnabled(options.enabled, query) !== false && query.state.data === void 0 && !(query.state.status === "error" && options.retryOnMount === false);
}
function shouldFetchOnMount(query, options) {
  return shouldLoadOnMount(query, options) || query.state.data !== void 0 && shouldFetchOn(query, options, options.refetchOnMount);
}
function shouldFetchOn(query, options, field) {
  if (resolveEnabled(options.enabled, query) !== false && resolveStaleTime(options.staleTime, query) !== "static") {
    const value = typeof field === "function" ? field(query) : field;
    return value === "always" || value !== false && isStale(query, options);
  }
  return false;
}
function shouldFetchOptionally(query, prevQuery, options, prevOptions) {
  return (query !== prevQuery || resolveEnabled(prevOptions.enabled, query) === false) && (!options.suspense || query.state.status !== "error") && isStale(query, options);
}
function isStale(query, options) {
  return resolveEnabled(options.enabled, query) !== false && query.isStaleByTime(resolveStaleTime(options.staleTime, query));
}
function shouldAssignObserverCurrentProperties(observer, optimisticResult) {
  if (!shallowEqualObjects(observer.getCurrentResult(), optimisticResult)) {
    return true;
  }
  return false;
}
var jsxRuntime = { exports: {} };
var reactJsxRuntime_production = {};
/**
 * @license React
 * react-jsx-runtime.production.js
 *
 * Copyright (c) Meta Platforms, Inc. and affiliates.
 *
 * This source code is licensed under the MIT license found in the
 * LICENSE file in the root directory of this source tree.
 */
var hasRequiredReactJsxRuntime_production;
function requireReactJsxRuntime_production() {
  if (hasRequiredReactJsxRuntime_production) return reactJsxRuntime_production;
  hasRequiredReactJsxRuntime_production = 1;
  var REACT_ELEMENT_TYPE = Symbol.for("react.transitional.element"), REACT_FRAGMENT_TYPE = Symbol.for("react.fragment");
  function jsxProd(type, config, maybeKey) {
    var key = null;
    void 0 !== maybeKey && (key = "" + maybeKey);
    void 0 !== config.key && (key = "" + config.key);
    if ("key" in config) {
      maybeKey = {};
      for (var propName in config)
        "key" !== propName && (maybeKey[propName] = config[propName]);
    } else maybeKey = config;
    config = maybeKey.ref;
    return {
      $$typeof: REACT_ELEMENT_TYPE,
      type,
      key,
      ref: void 0 !== config ? config : null,
      props: maybeKey
    };
  }
  reactJsxRuntime_production.Fragment = REACT_FRAGMENT_TYPE;
  reactJsxRuntime_production.jsx = jsxProd;
  reactJsxRuntime_production.jsxs = jsxProd;
  return reactJsxRuntime_production;
}
var hasRequiredJsxRuntime;
function requireJsxRuntime() {
  if (hasRequiredJsxRuntime) return jsxRuntime.exports;
  hasRequiredJsxRuntime = 1;
  {
    jsxRuntime.exports = requireReactJsxRuntime_production();
  }
  return jsxRuntime.exports;
}
var jsxRuntimeExports = requireJsxRuntime();
const React$4 = window["React"];
var QueryClientContext = React$4.createContext(
  void 0
);
var useQueryClient = (queryClient) => {
  const client = React$4.useContext(QueryClientContext);
  if (queryClient) {
    return queryClient;
  }
  if (!client) {
    throw new Error("No QueryClient set, use QueryClientProvider to set one");
  }
  return client;
};
const React$3 = window["React"];
var IsRestoringContext = React$3.createContext(false);
var useIsRestoring = () => React$3.useContext(IsRestoringContext);
IsRestoringContext.Provider;
const React$2 = window["React"];
function createValue() {
  let isReset = false;
  return {
    clearReset: () => {
      isReset = false;
    },
    reset: () => {
      isReset = true;
    },
    isReset: () => {
      return isReset;
    }
  };
}
var QueryErrorResetBoundaryContext = React$2.createContext(createValue());
var useQueryErrorResetBoundary = () => React$2.useContext(QueryErrorResetBoundaryContext);
const React$1 = window["React"];
var ensurePreventErrorBoundaryRetry = (options, errorResetBoundary) => {
  if (options.suspense || options.throwOnError || options.experimental_prefetchInRender) {
    if (!errorResetBoundary.isReset()) {
      options.retryOnMount = false;
    }
  }
};
var useClearResetErrorBoundary = (errorResetBoundary) => {
  React$1.useEffect(() => {
    errorResetBoundary.clearReset();
  }, [errorResetBoundary]);
};
var getHasError = ({
  result,
  errorResetBoundary,
  throwOnError,
  query,
  suspense
}) => {
  return result.isError && !errorResetBoundary.isReset() && !result.isFetching && query && (suspense && result.data === void 0 || shouldThrowError(throwOnError, [result.error, query]));
};
var ensureSuspenseTimers = (defaultedOptions) => {
  if (defaultedOptions.suspense) {
    const MIN_SUSPENSE_TIME_MS = 1e3;
    const clamp = (value) => value === "static" ? value : Math.max(value ?? MIN_SUSPENSE_TIME_MS, MIN_SUSPENSE_TIME_MS);
    const originalStaleTime = defaultedOptions.staleTime;
    defaultedOptions.staleTime = typeof originalStaleTime === "function" ? (...args) => clamp(originalStaleTime(...args)) : clamp(originalStaleTime);
    if (typeof defaultedOptions.gcTime === "number") {
      defaultedOptions.gcTime = Math.max(
        defaultedOptions.gcTime,
        MIN_SUSPENSE_TIME_MS
      );
    }
  }
};
var willFetch = (result, isRestoring) => result.isLoading && result.isFetching && !isRestoring;
var shouldSuspend = (defaultedOptions, result) => (defaultedOptions == null ? void 0 : defaultedOptions.suspense) && result.isPending;
var fetchOptimistic = (defaultedOptions, observer, errorResetBoundary) => observer.fetchOptimistic(defaultedOptions).catch(() => {
  errorResetBoundary.clearReset();
});
const React = window["React"];
function useBaseQuery(options, Observer, queryClient) {
  var _a2, _b2, _c2, _d, _e;
  const isRestoring = useIsRestoring();
  const errorResetBoundary = useQueryErrorResetBoundary();
  const client = useQueryClient(queryClient);
  const defaultedOptions = client.defaultQueryOptions(options);
  (_b2 = (_a2 = client.getDefaultOptions().queries) == null ? void 0 : _a2._experimental_beforeQuery) == null ? void 0 : _b2.call(
    _a2,
    defaultedOptions
  );
  defaultedOptions._optimisticResults = isRestoring ? "isRestoring" : "optimistic";
  ensureSuspenseTimers(defaultedOptions);
  ensurePreventErrorBoundaryRetry(defaultedOptions, errorResetBoundary);
  useClearResetErrorBoundary(errorResetBoundary);
  const isNewCacheEntry = !client.getQueryCache().get(defaultedOptions.queryHash);
  const [observer] = React.useState(
    () => new Observer(
      client,
      defaultedOptions
    )
  );
  const result = observer.getOptimisticResult(defaultedOptions);
  const shouldSubscribe = !isRestoring && options.subscribed !== false;
  React.useSyncExternalStore(
    React.useCallback(
      (onStoreChange) => {
        const unsubscribe = shouldSubscribe ? observer.subscribe(notifyManager.batchCalls(onStoreChange)) : noop;
        observer.updateResult();
        return unsubscribe;
      },
      [observer, shouldSubscribe]
    ),
    () => observer.getCurrentResult(),
    () => observer.getCurrentResult()
  );
  React.useEffect(() => {
    observer.setOptions(defaultedOptions);
  }, [defaultedOptions, observer]);
  if (shouldSuspend(defaultedOptions, result)) {
    throw fetchOptimistic(defaultedOptions, observer, errorResetBoundary);
  }
  if (getHasError({
    result,
    errorResetBoundary,
    throwOnError: defaultedOptions.throwOnError,
    query: client.getQueryCache().get(defaultedOptions.queryHash),
    suspense: defaultedOptions.suspense
  })) {
    throw result.error;
  }
  (_d = (_c2 = client.getDefaultOptions().queries) == null ? void 0 : _c2._experimental_afterQuery) == null ? void 0 : _d.call(
    _c2,
    defaultedOptions,
    result
  );
  if (defaultedOptions.experimental_prefetchInRender && !isServer && willFetch(result, isRestoring)) {
    const promise = isNewCacheEntry ? (
      // Fetch immediately on render in order to ensure `.promise` is resolved even if the component is unmounted
      fetchOptimistic(defaultedOptions, observer, errorResetBoundary)
    ) : (
      // subscribe to the "cache promise" so that we can finalize the currentThenable once data comes in
      (_e = client.getQueryCache().get(defaultedOptions.queryHash)) == null ? void 0 : _e.promise
    );
    promise == null ? void 0 : promise.catch(noop).finally(() => {
      observer.updateResult();
    });
  }
  return !defaultedOptions.notifyOnChangeProps ? observer.trackResult(result) : result;
}
function useQuery(options, queryClient) {
  return useBaseQuery(options, QueryObserver, queryClient);
}
const useRef$4 = window["React"].useRef;
const useEffect$7 = window["React"].useEffect;
const useMemo$2 = window["React"].useMemo;
function useCallbackRef(callback) {
  const callbackRef = useRef$4(callback);
  useEffect$7(() => {
    callbackRef.current = callback;
  });
  return useMemo$2(() => (...args) => {
    var _a2;
    return (_a2 = callbackRef.current) == null ? void 0 : _a2.call(callbackRef, ...args);
  }, []);
}
const useRef$3 = window["React"].useRef;
const useMemo$1 = window["React"].useMemo;
const useEffect$6 = window["React"].useEffect;
function useDebouncedCallback(callback, options) {
  const { delay, flushOnUnmount, leading } = { delay: options, flushOnUnmount: false, leading: false };
  const handleCallback = useCallbackRef(callback);
  const debounceTimerRef = useRef$3(0);
  const lastCallback = useMemo$1(() => {
    const currentCallback = Object.assign(
      (...args) => {
        window.clearTimeout(debounceTimerRef.current);
        const isFirstCall = currentCallback._isFirstCall;
        currentCallback._isFirstCall = false;
        function clearTimeoutAndLeadingRef() {
          window.clearTimeout(debounceTimerRef.current);
          debounceTimerRef.current = 0;
          currentCallback._isFirstCall = true;
        }
        if (leading && isFirstCall) {
          handleCallback(...args);
          const resetLeadingState = () => {
            clearTimeoutAndLeadingRef();
          };
          const flush2 = () => {
            if (debounceTimerRef.current !== 0) {
              clearTimeoutAndLeadingRef();
              handleCallback(...args);
            }
          };
          const cancel2 = () => {
            clearTimeoutAndLeadingRef();
          };
          currentCallback.flush = flush2;
          currentCallback.cancel = cancel2;
          debounceTimerRef.current = window.setTimeout(resetLeadingState, delay);
          return;
        }
        if (leading && !isFirstCall) {
          const flush2 = () => {
            if (debounceTimerRef.current !== 0) {
              clearTimeoutAndLeadingRef();
              handleCallback(...args);
            }
          };
          const cancel2 = () => {
            clearTimeoutAndLeadingRef();
          };
          currentCallback.flush = flush2;
          currentCallback.cancel = cancel2;
          const resetLeadingState = () => {
            clearTimeoutAndLeadingRef();
          };
          debounceTimerRef.current = window.setTimeout(resetLeadingState, delay);
          return;
        }
        const flush = () => {
          if (debounceTimerRef.current !== 0) {
            clearTimeoutAndLeadingRef();
            handleCallback(...args);
          }
        };
        const cancel = () => {
          clearTimeoutAndLeadingRef();
        };
        currentCallback.flush = flush;
        currentCallback.cancel = cancel;
        debounceTimerRef.current = window.setTimeout(flush, delay);
      },
      {
        flush: () => {
        },
        cancel: () => {
        },
        _isFirstCall: true
      }
    );
    return currentCallback;
  }, [handleCallback, delay, leading]);
  useEffect$6(
    () => () => {
      if (flushOnUnmount) {
        lastCallback.flush();
      } else {
        lastCallback.cancel();
      }
    },
    [lastCallback, flushOnUnmount]
  );
  return lastCallback;
}
const useRef$2 = window["React"].useRef;
const useEffect$5 = window["React"].useEffect;
const DEFAULT_EVENTS = ["mousedown", "touchstart"];
function useClickOutside(callback, events, nodes) {
  const ref = useRef$2(null);
  const eventsList = DEFAULT_EVENTS;
  useEffect$5(() => {
    const listener = (event) => {
      const { target } = event ?? {};
      if (Array.isArray(nodes)) {
        const shouldIgnore = !document.body.contains(target) && target.tagName !== "HTML";
        const shouldTrigger = nodes.every((node) => !!node && !event.composedPath().includes(node));
        shouldTrigger && !shouldIgnore && callback();
      } else if (ref.current && !ref.current.contains(target)) {
        callback();
      }
    };
    eventsList.forEach((fn) => document.addEventListener(fn, listener));
    return () => {
      eventsList.forEach((fn) => document.removeEventListener(fn, listener));
    };
  }, [ref, callback, nodes]);
  return ref;
}
const useState$3 = window["React"].useState;
const useEffect$4 = window["React"].useEffect;
function attachMediaListener(query, callback) {
  try {
    query.addEventListener("change", callback);
    return () => query.removeEventListener("change", callback);
  } catch (e) {
    query.addListener(callback);
    return () => query.removeListener(callback);
  }
}
function getInitialValue(query, initialValue) {
  if (typeof window !== "undefined" && "matchMedia" in window) {
    return window.matchMedia(query).matches;
  }
  return false;
}
function useMediaQuery(query, initialValue, { getInitialValueInEffect } = {
  getInitialValueInEffect: true
}) {
  const [matches, setMatches] = useState$3(
    getInitialValueInEffect ? initialValue : getInitialValue(query)
  );
  useEffect$4(() => {
    try {
      const mediaQuery = window.matchMedia(query);
      setMatches(mediaQuery.matches);
      return attachMediaListener(mediaQuery, (event) => setMatches(event.matches));
    } catch (e) {
      return void 0;
    }
  }, [query]);
  return matches || false;
}
const useEffect$3 = window["React"].useEffect;
function useWindowEvent(type, listener, options) {
  useEffect$3(() => {
    window.addEventListener(type, listener, options);
    return () => window.removeEventListener(type, listener, options);
  }, [type, listener]);
}
const useCallback$3 = window["React"].useCallback;
const useState$2 = window["React"].useState;
const useEffect$2 = window["React"].useEffect;
function serializeJSON(value, hookName = "use-local-storage") {
  try {
    return JSON.stringify(value);
  } catch (error) {
    throw new Error(`@mantine/hooks ${hookName}: Failed to serialize the value`);
  }
}
function deserializeJSON(value) {
  try {
    return value && JSON.parse(value);
  } catch {
    return value;
  }
}
function createStorageHandler(type) {
  const getItem = (key) => {
    try {
      return window[type].getItem(key);
    } catch (error) {
      console.warn("use-local-storage: Failed to get value from storage, localStorage is blocked");
      return null;
    }
  };
  const setItem = (key, value) => {
    try {
      window[type].setItem(key, value);
    } catch (error) {
      console.warn("use-local-storage: Failed to set value to storage, localStorage is blocked");
    }
  };
  const removeItem = (key) => {
    try {
      window[type].removeItem(key);
    } catch (error) {
      console.warn(
        "use-local-storage: Failed to remove value from storage, localStorage is blocked"
      );
    }
  };
  return { getItem, setItem, removeItem };
}
function createStorage(type, hookName) {
  const eventName = "mantine-local-storage";
  const { getItem, setItem, removeItem } = createStorageHandler(type);
  return function useStorage({
    key,
    defaultValue,
    getInitialValueInEffect = true,
    sync = true,
    deserialize = deserializeJSON,
    serialize = (value) => serializeJSON(value, hookName)
  }) {
    const readStorageValue = useCallback$3(
      (skipStorage) => {
        let storageBlockedOrSkipped;
        try {
          storageBlockedOrSkipped = typeof window === "undefined" || !(type in window) || window[type] === null || !!skipStorage;
        } catch (_e) {
          storageBlockedOrSkipped = true;
        }
        if (storageBlockedOrSkipped) {
          return defaultValue;
        }
        const storageValue = getItem(key);
        return storageValue !== null ? deserialize(storageValue) : defaultValue;
      },
      [key, defaultValue]
    );
    const [value, setValue] = useState$2(readStorageValue(getInitialValueInEffect));
    const setStorageValue = useCallback$3(
      (val) => {
        if (val instanceof Function) {
          setValue((current) => {
            const result = val(current);
            setItem(key, serialize(result));
            queueMicrotask(() => {
              window.dispatchEvent(
                new CustomEvent(eventName, { detail: { key, value: val(current) } })
              );
            });
            return result;
          });
        } else {
          setItem(key, serialize(val));
          window.dispatchEvent(new CustomEvent(eventName, { detail: { key, value: val } }));
          setValue(val);
        }
      },
      [key]
    );
    const removeStorageValue = useCallback$3(() => {
      removeItem(key);
      window.dispatchEvent(new CustomEvent(eventName, { detail: { key, value: defaultValue } }));
    }, []);
    useWindowEvent("storage", (event) => {
      if (sync) {
        if (event.storageArea === window[type] && event.key === key) {
          setValue(deserialize(event.newValue ?? void 0));
        }
      }
    });
    useWindowEvent(eventName, (event) => {
      if (sync) {
        if (event.detail.key === key) {
          setValue(event.detail.value);
        }
      }
    });
    useEffect$2(() => {
      if (defaultValue !== void 0 && value === void 0) {
        setStorageValue(defaultValue);
      }
    }, [defaultValue, value, setStorageValue]);
    useEffect$2(() => {
      const val = readStorageValue();
      val !== void 0 && setStorageValue(val);
    }, [key]);
    return [value === void 0 ? defaultValue : value, setStorageValue, removeStorageValue];
  };
}
function useLocalStorage(props) {
  return createStorage("localStorage", "use-local-storage")(props);
}
const useCallback$2 = window["React"].useCallback;
function assignRef(ref, value) {
  if (typeof ref === "function") {
    return ref(value);
  } else if (typeof ref === "object" && ref !== null && "current" in ref) {
    ref.current = value;
  }
}
function mergeRefs(...refs) {
  const cleanupMap = /* @__PURE__ */ new Map();
  return (node) => {
    refs.forEach((ref) => {
      const cleanup = assignRef(ref, node);
      if (cleanup) {
        cleanupMap.set(ref, cleanup);
      }
    });
    if (cleanupMap.size > 0) {
      return () => {
        refs.forEach((ref) => {
          const cleanup = cleanupMap.get(ref);
          if (cleanup && typeof cleanup === "function") {
            cleanup();
          } else {
            assignRef(ref, null);
          }
        });
        cleanupMap.clear();
      };
    }
  };
}
function useMergedRef(...refs) {
  return useCallback$2(mergeRefs(...refs), refs);
}
const useRef$1 = window["React"].useRef;
const useState$1 = window["React"].useState;
const useMemo = window["React"].useMemo;
const useEffect$1 = window["React"].useEffect;
const defaultState = {
  x: 0,
  y: 0,
  width: 0,
  height: 0,
  top: 0,
  left: 0,
  bottom: 0,
  right: 0
};
function useResizeObserver(options) {
  const frameID = useRef$1(0);
  const ref = useRef$1(null);
  const [rect, setRect] = useState$1(defaultState);
  const observer = useMemo(
    () => typeof window !== "undefined" ? new ResizeObserver((entries) => {
      const entry = entries[0];
      if (entry) {
        cancelAnimationFrame(frameID.current);
        frameID.current = requestAnimationFrame(() => {
          var _a2, _b2;
          if (ref.current) {
            const boxSize = ((_a2 = entry.borderBoxSize) == null ? void 0 : _a2[0]) || ((_b2 = entry.contentBoxSize) == null ? void 0 : _b2[0]);
            if (boxSize) {
              const width = boxSize.inlineSize;
              const height = boxSize.blockSize;
              setRect({
                width,
                height,
                x: entry.contentRect.x,
                y: entry.contentRect.y,
                top: entry.contentRect.top,
                left: entry.contentRect.left,
                bottom: entry.contentRect.bottom,
                right: entry.contentRect.right
              });
            } else {
              setRect(entry.contentRect);
            }
          }
        });
      }
    }) : null,
    []
  );
  useEffect$1(() => {
    if (ref.current) {
      observer == null ? void 0 : observer.observe(ref.current, options);
    }
    return () => {
      observer == null ? void 0 : observer.disconnect();
      if (frameID.current) {
        cancelAnimationFrame(frameID.current);
      }
    };
  }, [ref.current]);
  return [ref, rect];
}
const useState = window["React"].useState;
const useCallback$1 = window["React"].useCallback;
function useDisclosure(initialState = false, options = {}) {
  const [opened, setOpened] = useState(initialState);
  const open = useCallback$1(() => {
    setOpened((isOpened) => {
      var _a2;
      if (!isOpened) {
        (_a2 = options.onOpen) == null ? void 0 : _a2.call(options);
        return true;
      }
      return isOpened;
    });
  }, [options.onOpen]);
  const close = useCallback$1(() => {
    setOpened((isOpened) => {
      var _a2;
      if (isOpened) {
        (_a2 = options.onClose) == null ? void 0 : _a2.call(options);
        return false;
      }
      return isOpened;
    });
  }, [options.onClose]);
  const toggle = useCallback$1(() => {
    opened ? close() : open();
  }, [close, open, opened]);
  return [opened, { open, close, toggle }];
}
const useRef = window["React"].useRef;
const useCallback = window["React"].useCallback;
const useEffect = window["React"].useEffect;
function useTimeout(callback, delay, options = { autoInvoke: false }) {
  const timeoutRef = useRef(null);
  const start = useCallback(
    (...args) => {
      if (!timeoutRef.current) {
        timeoutRef.current = window.setTimeout(() => {
          callback(args);
          timeoutRef.current = null;
        }, delay);
      }
    },
    [delay]
  );
  const clear = useCallback(() => {
    if (timeoutRef.current) {
      window.clearTimeout(timeoutRef.current);
      timeoutRef.current = null;
    }
  }, []);
  useEffect(() => {
    if (options.autoInvoke) {
      start();
    }
    return clear;
  }, [clear, start]);
  return { start, clear };
}
function r(e) {
  var t, f, n = "";
  if ("string" == typeof e || "number" == typeof e) n += e;
  else if ("object" == typeof e) if (Array.isArray(e)) {
    var o = e.length;
    for (t = 0; t < o; t++) e[t] && (f = r(e[t])) && (n && (n += " "), n += f);
  } else for (f in e) e[f] && (n && (n += " "), n += f);
  return n;
}
function clsx() {
  for (var e, t, f = 0, n = "", o = arguments.length; f < o; f++) (e = arguments[f]) && (t = r(e)) && (n && (n += " "), n += t);
  return n;
}
const Kr = window["MantineCore"].Box;
const Jr = window["MantineCore"].Table;
const ke = window["React"].useCallback;
const Yr = window["React"].useMemo;
const Ke = window["React"].useState;
const kt = window["React"].useState;
const $a = window["MantineCore"].createSafeContext;
var [Mt, de] = $a("useDataTableColumnsContext must be used within DataTableColumnProvider");
var at = (e) => {
  let { children: t, columnsOrder: o, setColumnsOrder: n, columnsToggle: a, setColumnsToggle: r2, resetColumnsOrder: l, resetColumnsToggle: i, setColumnWidth: s, resetColumnsWidth: d } = e, [m, b] = kt(""), [p, T] = kt("");
  return jsxRuntimeExports.jsx(Mt, { value: { sourceColumn: m, setSourceColumn: b, targetColumn: p, setTargetColumn: T, columnsToggle: a, setColumnsToggle: r2, swapColumns: () => {
    if (!o || !n || !m || !p) return;
    let x = o.indexOf(m), D = o.indexOf(p);
    if (x !== -1 && D !== -1) {
      let S = o.splice(x, 1)[0];
      o.splice(D, 0, S), n([...o]);
    }
  }, resetColumnsOrder: l, resetColumnsToggle: i, setColumnWidth: s, resetColumnsWidth: d }, children: t });
};
function Nt() {
  return jsxRuntimeExports.jsx("tr", { className: "mantine-datatable-empty-row", children: jsxRuntimeExports.jsx("td", {}) });
}
const Za = window["MantineCore"].Center;
const Ya = window["MantineCore"].Text;
function Lt() {
  return jsxRuntimeExports.jsxs("svg", { width: "24", height: "24", viewBox: "0 0 24 24", strokeWidth: "2", stroke: "currentColor", fill: "none", strokeLinecap: "round", strokeLinejoin: "round", children: [jsxRuntimeExports.jsx("path", { stroke: "none", d: "M0 0h24v24H0z", fill: "none" }), jsxRuntimeExports.jsx("path", { d: "M12.983 8.978c3.955 -.182 7.017 -1.446 7.017 -2.978c0 -1.657 -3.582 -3 -8 -3c-1.661 0 -3.204 .19 -4.483 .515m-2.783 1.228c-.471 .382 -.734 .808 -.734 1.257c0 1.22 1.944 2.271 4.734 2.74" }), jsxRuntimeExports.jsx("path", { d: "M4 6v6c0 1.657 3.582 3 8 3c.986 0 1.93 -.067 2.802 -.19m3.187 -.82c1.251 -.53 2.011 -1.228 2.011 -1.99v-6" }), jsxRuntimeExports.jsx("path", { d: "M4 12v6c0 1.657 3.582 3 8 3c3.217 0 5.991 -.712 7.261 -1.74m.739 -3.26v-4" }), jsxRuntimeExports.jsx("path", { d: "M3 3l18 18" })] });
}
function Ht({ icon: e, text: t, pt: o, pb: n, active: a, children: r2 }) {
  return jsxRuntimeExports.jsx(Za, { pt: o, pb: n, className: "mantine-datatable-empty-state", "data-active": a || void 0, children: r2 || jsxRuntimeExports.jsxs(jsxRuntimeExports.Fragment, { children: [e || jsxRuntimeExports.jsx("div", { className: "mantine-datatable-empty-state-icon", children: jsxRuntimeExports.jsx(Lt, {}) }), jsxRuntimeExports.jsx(Ya, { component: "div", size: "sm", c: "dimmed", children: t })] }) });
}
const wn = window["MantineCore"].TableTfoot;
const Sn = window["MantineCore"].TableTr;
const Pn = window["MantineCore"].rem;
const vn = window["React"].forwardRef;
const gn = window["MantineCore"].TableTh;
const en = window["React"].useMemo;
var It = ({ key: e, columns: t = [], getInitialValueInEffect: o = true }) => {
  function n(c, y) {
    let f = [];
    return c.forEach((u) => {
      y.find((w) => w.accessor === u) && f.push(u);
    }), y.forEach((u) => {
      f.includes(u.accessor) || f.push(u.accessor);
    }), f;
  }
  function a(c, y) {
    let f = [];
    return c.forEach((u) => {
      y.find((w) => w.accessor === u.accessor) && f.push(u);
    }), y.forEach((u) => {
      f.find((w) => w.accessor === u.accessor) || f.push({ accessor: u.accessor, defaultToggle: u.defaultToggle || true, toggleable: u.toggleable, toggled: u.defaultToggle === void 0 ? true : u.defaultToggle });
    }), f;
  }
  function r2(c, y) {
    let f = [];
    return c.forEach((u) => {
      let w = Object.keys(u)[0];
      y.find((h) => h.accessor === w) && f.push(u);
    }), y.forEach((u) => {
      let w = u.accessor;
      if (!f.find((h) => Object.keys(h)[0] === w)) {
        let h = {};
        h[w] = "", f.push(h);
      }
    }), f;
  }
  function l() {
    let [c, y] = useLocalStorage({ key: e ? `${e}-columns-order` : "", defaultValue: e ? d : void 0, getInitialValueInEffect: o });
    function f(h) {
      e && y(h);
    }
    if (!e) return [c, f];
    let u = n(c, t), w = JSON.stringify(c);
    return JSON.stringify(u) !== w && f(u), [u, f];
  }
  function i() {
    let [c, y] = useLocalStorage({ key: e ? `${e}-columns-toggle` : "", defaultValue: e ? b : void 0, getInitialValueInEffect: o });
    function f(h) {
      e && y(h);
    }
    if (!e) return [c, f];
    let u = a(c, t), w = JSON.stringify(c);
    return JSON.stringify(u) !== w && f(u), [a(c, t), f];
  }
  function s() {
    let [c, y] = useLocalStorage({ key: e ? `${e}-columns-width` : "", defaultValue: e ? m : void 0, getInitialValueInEffect: o });
    function f(h) {
      e && y(h);
    }
    if (!e) return [c, f];
    let u = r2(c, t), w = JSON.stringify(c);
    return JSON.stringify(u) !== w && f(u), [r2(c, t), f];
  }
  let d = t && t.map((c) => c.accessor) || [], m = t && t.map((c) => ({ [c.accessor]: c.width ?? "initial" })) || [], b = t && t.map((c) => ({ accessor: c.accessor, defaultToggle: c.defaultToggle || true, toggleable: c.toggleable, toggled: c.defaultToggle === void 0 ? true : c.defaultToggle })), [p, T] = l(), [g, x] = i(), [D, S] = s(), R = () => T(d), P = () => {
    x(b);
  }, M = () => S(m);
  return { effectiveColumns: en(() => p ? p.map((f) => t.find((u) => u.accessor === f)).map((f) => {
    var _a2;
    return { ...f, hidden: (f == null ? void 0 : f.hidden) || !((_a2 = g.find((u) => u.accessor === (f == null ? void 0 : f.accessor))) == null ? void 0 : _a2.toggled) };
  }).map((f) => {
    var _a2;
    return { ...f, width: (_a2 = D.find((u) => u[f == null ? void 0 : f.accessor])) == null ? void 0 : _a2[f == null ? void 0 : f.accessor] };
  }) : t, [t, p, g, D]), setColumnsOrder: T, columnsOrder: p, resetColumnsOrder: R, columnsToggle: g, setColumnsToggle: x, resetColumnsToggle: P, columnsWidth: D, setColumnsWidth: S, setColumnWidth: (c, y) => {
    let f = D.map((u) => u[c] ? { [c]: y } : u);
    S(f);
  }, resetColumnsWidth: M };
};
function ne() {
  var _a2;
  let [e] = useResizeObserver(), { width: t, height: o } = ((_a2 = e.current) == null ? void 0 : _a2.getBoundingClientRect()) || { width: 0, height: 0 };
  return { ref: e, width: t, height: o };
}
const on = window["React"].useEffect;
const an = window["React"].useLayoutEffect;
var Ot = typeof window < "u" ? an : on;
const nn = window["React"].useEffect;
const rn = window["React"].useState;
function Wt(e) {
  let [t, o] = rn(null), n = (e == null ? void 0 : e.join(":")) || "";
  return nn(() => {
    o(null);
  }, [n]), { lastSelectionChangeIndex: t, setLastSelectionChangeIndex: o };
}
const ln = window["React"].useEffect;
const sn = window["React"].useRef;
const dn = window["React"].useState;
function cn(e, t) {
  let o = () => {
    t(e.map((a) => a.matches));
  }, n = e.map((a) => {
    try {
      return a.addEventListener("change", o), () => a.removeEventListener("change", o);
    } catch {
      return a.addListener(o), () => a.removeListener(o);
    }
  });
  return () => {
    n.forEach((a) => a());
  };
}
function un(e, t) {
  return t || (typeof window < "u" && "matchMedia" in window ? e.map((o) => window.matchMedia(o).matches) : e.map(() => false));
}
function At(e, t, { getInitialValueInEffect: o } = { getInitialValueInEffect: true }) {
  let [n, a] = dn(o ? t : un(e, t)), r2 = sn(null);
  return ln(() => {
    if ("matchMedia" in window) return r2.current = e.map((l) => window.matchMedia(l)), a(r2.current.map((l) => l.matches)), cn(r2.current, (l) => {
      a(l);
    });
  }, [e]), n;
}
const mn = window["MantineCore"].useMantineTheme;
const zt = window["React"].useMemo;
function Vt(e) {
  let t = mn(), o = zt(() => e.map((a) => (typeof a == "function" ? a(t) : a) ?? ""), [e, t]), n = zt(() => e.map(() => true), [e]);
  return At(o, n);
}
const pn = window["MantineCore"].useMantineTheme;
function K(e) {
  let t = pn(), o = typeof e == "function" ? e(t) : e;
  return useMediaQuery(o || "", true);
}
const bn = window["React"].useState;
function ce(e) {
  let t = e.replace(/([a-z\d])([A-Z]+)/g, "$1 $2").replace(/\W|_/g, " ").trim().toLowerCase();
  return `${t.charAt(0).toUpperCase()}${t.slice(1)}`;
}
function _t(e, t, o) {
  return e.filter((n) => !t.map(o).includes(o(n)));
}
function We(e, t) {
  return e.filter((o, n, a) => n === a.findIndex((r2) => t(o) === t(r2)));
}
function rt(e, t) {
  return t ? t.match(/([^[.\]])+/g).reduce((n, a) => n && n[a], e) : void 0;
}
function E(e, t) {
  return typeof t == "string" ? rt(e, t) : t(e);
}
function Ft({ rowExpansion: e, records: t, idAccessor: o }) {
  let n = [];
  if (e && t) {
    let { trigger: i, allowMultiple: s, initiallyExpanded: d } = e;
    t && i === "always" ? n = t.map((m) => E(m, o)) : d && (n = t.filter((m, b) => d({ record: m, index: b })).map((m) => E(m, o)), s || (n = [n[0]]));
  }
  let a, r2, l = bn(n);
  if (e) {
    let { expandable: i, trigger: s, allowMultiple: d, collapseProps: m, content: b } = e;
    e.expanded ? { recordIds: a, onRecordIdsChange: r2 } = e.expanded : [a, r2] = l;
    let p = (T) => r2 == null ? void 0 : r2(a.filter((g) => g !== E(T, o)));
    return { expandOnClick: s !== "always" && s !== "never", isRowExpanded: (T) => s === "always" ? true : a.includes(E(T, o)), isExpandable: ({ record: T, index: g }) => i ? i({ record: T, index: g }) : true, expandRow: (T) => {
      let g = E(T, o);
      r2 == null ? void 0 : r2(d ? [...a, g] : [g]);
    }, collapseRow: p, collapseProps: m, content: ({ record: T, index: g }) => () => b({ record: T, index: g, collapse: () => p(T) }) };
  }
}
const Tn = window["React"].useEffect;
const Gt = window["React"].useState;
function Xt(e, t) {
  let [o, n] = Gt(e), [a, r2] = Gt(e), l = useTimeout(() => n(true), 0), i = useTimeout(() => r2(false), t || 200);
  return Tn(() => {
    e ? (i.clear(), r2(true), l.start()) : (l.clear(), n(false), i.start());
  }, [l, i, e]), { expanded: o, visible: a };
}
var ue = "mantine-datatable-nowrap", me = "mantine-datatable-ellipsis", B = "mantine-datatable-pointer-cursor", Ae = "mantine-datatable-context-menu-cursor", Qt = "mantine-datatable-text-selection-disabled", J = "mantine-datatable-text-align-left", Z = "mantine-datatable-text-align-center", Y = "mantine-datatable-text-align-right";
function Ut({ className: e, style: t, visibleMediaQuery: o, title: n, noWrap: a, ellipsis: r2, textAlign: l, width: i }) {
  return K(o) ? jsxRuntimeExports.jsx(gn, { className: clsx({ [ue]: a || r2, [me]: r2, [J]: l === "left", [Z]: l === "center", [Y]: l === "right" }, e), style: [{ width: i, minWidth: i, maxWidth: i }, t], children: n }) : null;
}
const Dn = window["MantineCore"].TableTh;
function $t({ shadowVisible: e }) {
  return jsxRuntimeExports.jsx(Dn, { className: "mantine-datatable-footer-selector-placeholder-cell", "data-shadow-visible": e || void 0 });
}
var Kt = vn(function({ className: t, style: o, columns: n, defaultColumnProps: a, selectionVisible: r2, selectorCellShadowVisible: l, scrollDiff: i }, s) {
  let d = i < 0;
  return jsxRuntimeExports.jsx(wn, { ref: s, className: clsx("mantine-datatable-footer", t), style: [{ position: d ? "relative" : "sticky", bottom: Pn(d ? i : 0) }, o], children: jsxRuntimeExports.jsxs(Sn, { children: [r2 && jsxRuntimeExports.jsx($t, { shadowVisible: l }), n.map(({ hidden: m, ...b }) => {
    if (m) return null;
    let { accessor: p, visibleMediaQuery: T, textAlign: g, width: x, footer: D, footerClassName: S, footerStyle: R, noWrap: P, ellipsis: M } = { ...a, ...b };
    return jsxRuntimeExports.jsx(Ut, { className: S, style: R, visibleMediaQuery: T, textAlign: g, width: x, title: D, noWrap: P, ellipsis: M }, p);
  })] }) });
});
const rr = window["MantineCore"].Checkbox;
const lr = window["MantineCore"].Group;
const ir = window["MantineCore"].Popover;
const sr = window["MantineCore"].PopoverDropdown;
const dr = window["MantineCore"].PopoverTarget;
const cr = window["MantineCore"].Stack;
const ur = window["MantineCore"].TableThead;
const mo = window["MantineCore"].TableTr;
const pr = window["React"].forwardRef;
const fr = window["React"].useState;
const Mn = window["MantineCore"].TableTh;
const Jt = window["React"].useMemo;
function Zt({ group: { id: e, columns: t, title: o, textAlign: n, className: a, style: r2 } }) {
  let l = Jt(() => t.map(({ visibleMediaQuery: d }) => d), [t]), i = Vt(l), s = Jt(() => t.filter(({ hidden: d }, m) => !d && (i == null ? void 0 : i[m])).length, [t, i]);
  return s > 0 ? jsxRuntimeExports.jsx(Mn, { colSpan: s, className: clsx("mantine-datatable-column-group-header-cell", { [J]: n === "left", [Z]: n === "center", [Y]: n === "right" }, a), style: r2, children: o ?? ce(e) }) : null;
}
const io = window["MantineCore"].ActionIcon;
const Kn = window["MantineCore"].Box;
const Fe = window["MantineCore"].Center;
const Jn = window["MantineCore"].Flex;
const Zn = window["MantineCore"].Group;
const Yn = window["MantineCore"].TableTh;
const qn = window["React"].useRef;
const jn = window["React"].useState;
const Hn = window["MantineCore"].ActionIcon;
const In = window["MantineCore"].Popover;
const On = window["MantineCore"].PopoverDropdown;
const Wn = window["MantineCore"].PopoverTarget;
function qt() {
  return jsxRuntimeExports.jsxs("svg", { width: "14", height: "14", viewBox: "0 0 24 24", strokeWidth: "2", stroke: "currentColor", fill: "none", strokeLinecap: "round", strokeLinejoin: "round", children: [jsxRuntimeExports.jsx("path", { stroke: "none", d: "M0 0h24v24H0z", fill: "none" }), jsxRuntimeExports.jsx("path", { d: "M4 4h16v2.172a2 2 0 0 1 -.586 1.414l-4.414 4.414v7l-6 2v-8.5l-4.48 -4.928a2 2 0 0 1 -.52 -1.345v-2.227z" })] });
}
function eo() {
  return jsxRuntimeExports.jsxs("svg", { width: "14", height: "14", viewBox: "0 0 24 24", strokeWidth: "2", stroke: "currentColor", fill: "none", strokeLinecap: "round", strokeLinejoin: "round", children: [jsxRuntimeExports.jsx("path", { stroke: "none", d: "M0 0h24v24H0z", fill: "none" }), jsxRuntimeExports.jsx("path", { d: "M20 3h-16a1 1 0 0 0 -1 1v2.227l.008 .223a3 3 0 0 0 .772 1.795l4.22 4.641v8.114a1 1 0 0 0 1.316 .949l6 -2l.108 -.043a1 1 0 0 0 .576 -.906v-6.586l4.121 -4.12a3 3 0 0 0 .879 -2.123v-2.171a1 1 0 0 0 -1 -1z", strokeWidth: "0", fill: "currentColor" })] });
}
function to({ children: e, isActive: t, filterPopoverProps: o }) {
  let [n, { close: a, toggle: r2 }] = useDisclosure(false), l = t ? eo : qt, i = useClickOutside(a);
  return jsxRuntimeExports.jsxs(In, { withArrow: true, shadow: "md", opened: n, onClose: a, trapFocus: true, ...o, children: [jsxRuntimeExports.jsx(Wn, { children: jsxRuntimeExports.jsx(Hn, { className: "mantine-datatable-header-cell-filter-action-icon", "data-active": t || void 0, size: "sm", variant: "default", onClick: (s) => {
    s.preventDefault(), r2();
  }, onKeyDown: (s) => s.stopPropagation(), children: jsxRuntimeExports.jsx(l, {}) }) }), jsxRuntimeExports.jsx(On, { ref: i, onClick: (s) => s.stopPropagation(), onKeyDown: (s) => s.stopPropagation(), children: typeof e == "function" ? e({ close: a }) : e })] });
}
const _n = window["MantineCore"].rem;
const Fn = window["React"].useRef;
const Bn = window["React"].useState;
var oo = (e) => {
  let { accessor: t, columnRef: o } = e, n = Fn(null), [a, r2] = Bn(0), { setColumnWidth: l } = de(), i = (b) => {
    b.preventDefault(), b.stopPropagation(), document.addEventListener("mousemove", s), document.addEventListener("mouseup", d), document.body.style.cursor = "col-resize";
  }, s = (b) => {
    if (!o.current) return;
    let p = b.clientX - o.current.getBoundingClientRect().right, g = `${o.current.getBoundingClientRect().width + p}px`;
    o.current.style.width = g, l(t, o.current.style.width), r2(-p);
  }, d = () => {
    o.current && (document.removeEventListener("mousemove", s), document.removeEventListener("mouseup", d), document.body.style.cursor = "initial", l(t, o.current.style.width), r2(0));
  };
  return jsxRuntimeExports.jsx("div", { ref: n, onClick: (b) => b.stopPropagation(), onMouseDown: i, onDoubleClick: () => {
    o.current && (o.current.style.maxWidth = "initial", o.current.style.minWidth = "initial", o.current.style.width = "initial", l(t, "initial"));
  }, className: "mantine-datatable-header-resizable-handle", style: { right: _n(a) } });
};
function ao() {
  return jsxRuntimeExports.jsxs("svg", { width: "14", height: "14", viewBox: "0 0 24 24", strokeWidth: "2", stroke: "currentColor", fill: "none", strokeLinecap: "round", strokeLinejoin: "round", children: [jsxRuntimeExports.jsx("path", { stroke: "none", d: "M0 0h24v24H0z", fill: "none" }), jsxRuntimeExports.jsx("path", { d: "M12 5l0 14" }), jsxRuntimeExports.jsx("path", { d: "M16 9l-4 -4" }), jsxRuntimeExports.jsx("path", { d: "M8 9l4 -4" })] });
}
function no() {
  return jsxRuntimeExports.jsxs("svg", { width: "14", height: "14", viewBox: "0 0 24 24", strokeWidth: "2", stroke: "currentColor", fill: "none", strokeLinecap: "round", strokeLinejoin: "round", children: [jsxRuntimeExports.jsx("path", { stroke: "none", d: "M0 0h24v24H0z", fill: "none" }), jsxRuntimeExports.jsx("path", { d: "M8 7l4 -4l4 4" }), jsxRuntimeExports.jsx("path", { d: "M8 17l4 4l4 -4" }), jsxRuntimeExports.jsx("path", { d: "M12 3l0 18" })] });
}
function ro() {
  return jsxRuntimeExports.jsxs("svg", { width: "14", height: "14", viewBox: "0 0 24 24", strokeWidth: "2", stroke: "currentColor", fill: "none", strokeLinecap: "round", strokeLinejoin: "round", children: [jsxRuntimeExports.jsx("path", { stroke: "none", d: "M0 0h24v24H0z", fill: "none" }), jsxRuntimeExports.jsx("path", { d: "M9 5m-1 0a1 1 0 1 0 2 0a1 1 0 1 0 -2 0" }), jsxRuntimeExports.jsx("path", { d: "M9 12m-1 0a1 1 0 1 0 2 0a1 1 0 1 0 -2 0" }), jsxRuntimeExports.jsx("path", { d: "M9 19m-1 0a1 1 0 1 0 2 0a1 1 0 1 0 -2 0" }), jsxRuntimeExports.jsx("path", { d: "M15 5m-1 0a1 1 0 1 0 2 0a1 1 0 1 0 -2 0" }), jsxRuntimeExports.jsx("path", { d: "M15 12m-1 0a1 1 0 1 0 2 0a1 1 0 1 0 -2 0" }), jsxRuntimeExports.jsx("path", { d: "M15 19m-1 0a1 1 0 1 0 2 0a1 1 0 1 0 -2 0" })] });
}
function lo() {
  return jsxRuntimeExports.jsxs("svg", { width: "14", height: "14", viewBox: "0 0 24 24", strokeWidth: "2", stroke: "currentColor", fill: "none", strokeLinecap: "round", strokeLinejoin: "round", children: [jsxRuntimeExports.jsx("path", { stroke: "none", d: "M0 0h24v24H0z", fill: "none" }), jsxRuntimeExports.jsx("path", { d: "M18 6l-12 12" }), jsxRuntimeExports.jsx("path", { d: "M6 6l12 12" })] });
}
function so({ className: e, style: t, accessor: o, visibleMediaQuery: n, title: a, sortable: r2, draggable: l, toggleable: i, resizable: s, sortIcons: d, textAlign: m, width: b, sortStatus: p, onSortStatusChange: T, filter: g, filterPopoverProps: x, filtering: D, sortKey: S }) {
  let { setSourceColumn: R, setTargetColumn: P, swapColumns: M, setColumnsToggle: N } = de(), [A, c] = jn(false), y = qn(null);
  if (!K(n)) return null;
  let f = a ?? ce(o), u = typeof f == "string" ? f : void 0, w = r2 && T ? (k) => {
    (k == null ? void 0 : k.defaultPrevented) || T({ sortKey: S, columnAccessor: o, direction: (p == null ? void 0 : p.columnAccessor) === o ? p.direction === "asc" ? "desc" : "asc" : (p == null ? void 0 : p.direction) ?? "asc" });
  } : void 0, h = (k) => {
    k.stopPropagation(), R(o), c(false);
  }, L = (k) => {
    k.preventDefault(), P(o), c(true);
  }, I = () => {
    P(o), c(false), M();
  }, z = () => {
    c(true);
  }, Q = () => {
    c(false);
  }, F = (k) => {
    k.stopPropagation(), N((U) => U.map((G) => G.accessor === o ? { ...G, toggled: false } : G));
  };
  return jsxRuntimeExports.jsxs(Yn, { className: clsx({ "mantine-datatable-header-cell-sortable": r2, "mantine-datatable-header-cell-toggleable": i, "mantine-datatable-header-cell-resizable": s }, e), style: [{ width: b, ...s ? { minWidth: "1px" } : { minWidth: b, maxWidth: b } }, t], role: r2 ? "button" : void 0, tabIndex: r2 ? 0 : void 0, onClick: w, onKeyDown: (k) => k.key === "Enter" && (w == null ? void 0 : w()), ref: y, children: [jsxRuntimeExports.jsxs(Zn, { className: "mantine-datatable-header-cell-sortable-group", justify: "space-between", wrap: "nowrap", children: [jsxRuntimeExports.jsxs(Jn, { align: "center", w: "100%", className: clsx({ "mantine-datatable-header-cell-draggable": l, "mantine-datatable-header-cell-drag-over": A }), draggable: l, onDragStart: l ? h : void 0, onDragEnter: l ? z : void 0, onDragOver: l ? L : void 0, onDrop: l ? I : void 0, onDragLeave: l ? Q : void 0, children: [l ? jsxRuntimeExports.jsx(Fe, { role: "img", "aria-label": "Drag column", children: jsxRuntimeExports.jsx(io, { className: "mantine-datatable-header-cell-draggable-action-icon", variant: "subtle", size: "xs", onClick: (k) => {
    k.stopPropagation();
  }, children: jsxRuntimeExports.jsx(ro, {}) }) }) : null, jsxRuntimeExports.jsx(Kn, { className: clsx("mantine-datatable-header-cell-sortable-text", { [J]: m === "left", [Z]: m === "center", [Y]: m === "right" }, ue, me), title: u, children: f })] }), i ? jsxRuntimeExports.jsx(Fe, { className: "mantine-datatable-header-cell-toggleable-icon", role: "img", "aria-label": "Toggle column", children: jsxRuntimeExports.jsx(io, { size: "xs", variant: "light", onClick: F, children: jsxRuntimeExports.jsx(lo, {}) }) }) : null, r2 || (p == null ? void 0 : p.columnAccessor) === o ? jsxRuntimeExports.jsx(jsxRuntimeExports.Fragment, { children: (p == null ? void 0 : p.columnAccessor) === o ? jsxRuntimeExports.jsx(Fe, { className: clsx("mantine-datatable-header-cell-sortable-icon", { "mantine-datatable-header-cell-sortable-icon-reversed": p.direction === "desc" }), role: "img", "aria-label": `Sorted ${p.direction === "desc" ? "descending" : "ascending"}`, children: (d == null ? void 0 : d.sorted) || jsxRuntimeExports.jsx(ao, {}) }) : jsxRuntimeExports.jsx(Fe, { className: "mantine-datatable-header-cell-sortable-unsorted-icon", role: "img", "aria-label": "Not sorted", children: (d == null ? void 0 : d.unsorted) || jsxRuntimeExports.jsx(no, {}) }) }) : null, g ? jsxRuntimeExports.jsx(to, { filterPopoverProps: x, isActive: !!D, children: g }) : null] }), s ? jsxRuntimeExports.jsx(oo, { accessor: o, columnRef: y }) : null] });
}
const tr = window["MantineCore"].Checkbox;
const or = window["MantineCore"].TableTh;
const nr = window["React"].forwardRef;
var uo = nr(function({ className: t, style: o, trigger: n, shadowVisible: a, checked: r2, indeterminate: l, checkboxProps: i, onChange: s, rowSpan: d }, m) {
  let b = !i.disabled;
  return jsxRuntimeExports.jsx(or, { ref: m, className: clsx("mantine-datatable-header-selector-cell", { [B]: n === "cell" && b }, t), style: o, rowSpan: d, "data-shadow-visible": a || void 0, onClick: n === "cell" && b ? s : void 0, children: jsxRuntimeExports.jsx(tr, { classNames: b ? { input: B } : void 0, checked: r2, indeterminate: l, onChange: s, ...i, disabled: !(s || i.onChange) || i.disabled }) });
});
var po = pr(function({ selectionColumnHeaderRef: t, className: o, style: n, sortStatus: a, sortIcons: r2, onSortStatusChange: l, columns: i, defaultColumnProps: s, groups: d, selectionTrigger: m, selectionVisible: b, selectionChecked: p, selectionIndeterminate: T, onSelectionChange: g, selectionCheckboxProps: x, selectorCellShadowVisible: D, selectionColumnClassName: S, selectionColumnStyle: R }, P) {
  let M = b ? jsxRuntimeExports.jsx(uo, { ref: t, className: S, style: R, trigger: m, shadowVisible: D, checked: p, indeterminate: T, checkboxProps: x, onChange: g, rowSpan: d ? 2 : void 0 }) : null, { columnsToggle: N, setColumnsToggle: A } = de(), [c, y] = fr(false), f = i.some((h) => h.toggleable), u = f ? Object.fromEntries(i.map(({ accessor: h, title: L }) => [h, L ?? ce(String(h))])) : void 0, w = jsxRuntimeExports.jsxs(ur, { className: clsx("mantine-datatable-header", o), style: n, ref: P, onContextMenu: f ? (h) => {
    h.preventDefault(), y((L) => !L);
  } : void 0, children: [d && jsxRuntimeExports.jsxs(mo, { children: [M, d.map((h) => jsxRuntimeExports.jsx(Zt, { group: h }, h.id))] }), jsxRuntimeExports.jsxs(mo, { children: [!d && M, i.map(({ hidden: h, ...L }, I) => {
    if (h) return null;
    let { accessor: z, visibleMediaQuery: Q, textAlign: F, width: k, title: U, sortable: G, draggable: pe, toggleable: fe, resizable: be, titleClassName: Te, titleStyle: ge, filter: j, filterPopoverProps: he, filtering: Ce, sortKey: X } = { ...s, ...L };
    return jsxRuntimeExports.jsx(so, { accessor: z, className: Te, style: ge, visibleMediaQuery: Q, textAlign: F, width: k, title: U, sortable: G, draggable: pe, toggleable: fe, resizable: be && I < i.length - 1, sortStatus: a, sortIcons: r2, sortKey: X, onSortStatusChange: l, filter: j, filterPopoverProps: he, filtering: Ce }, z);
  })] })] });
  return f ? jsxRuntimeExports.jsxs(ir, { position: "bottom", withArrow: true, shadow: "md", opened: c, onChange: y, children: [jsxRuntimeExports.jsx(dr, { children: w }), jsxRuntimeExports.jsx(sr, { children: jsxRuntimeExports.jsx(cr, { children: N.filter((h) => h.toggleable).map((h) => jsxRuntimeExports.jsx(lr, { children: jsxRuntimeExports.jsx(rr, { classNames: { label: "mantine-datatable-header-column-toggle-checkbox-label" }, size: "xs", label: u[h.accessor], checked: h.toggled, onChange: (L) => {
    A(N.map((I) => I.accessor === h.accessor ? { ...I, toggled: L.currentTarget.checked } : I));
  } }) }, h.accessor)) }) })] }) : w;
});
const br = window["MantineCore"].Center;
const Tr = window["MantineCore"].Loader;
function bo({ pt: e, pb: t, fetching: o, customContent: n, backgroundBlur: a, size: r2, type: l, color: i }) {
  return jsxRuntimeExports.jsx(br, { pt: e, pb: t, className: clsx("mantine-datatable-loader", { "mantine-datatable-loader-fetching": o }), style: [{ backdropFilter: a ? `blur(${a}px)` : void 0 }], children: o && (n || jsxRuntimeExports.jsx(Tr, { size: r2, type: l, color: i })) });
}
const Rr = window["MantineCore"].Box;
const Mr = window["MantineCore"].Pagination;
const kr = window["MantineCore"].Text;
const Er = window["MantineCore"].rem;
const Nr = window["React"].forwardRef;
const Dr = window["MantineCore"].Button;
const yr = window["MantineCore"].Group;
const wr = window["MantineCore"].Menu;
const Sr = window["MantineCore"].MenuDropdown;
const Pr = window["MantineCore"].MenuItem;
const xr = window["MantineCore"].MenuTarget;
const Co = window["MantineCore"].Text;
const Re = window["MantineCore"].rem;
const hr = window["MantineCore"].parseThemeColor;
function v(e, t, o) {
  return e ? hr({ color: typeof e == "object" ? e[o] : e, theme: t }).value : void 0;
}
function To({ theme: e, c: t, backgroundColor: o, borderColor: n, rowBorderColor: a, stripedColor: r2, highlightOnHoverColor: l }) {
  return { "--mantine-datatable-color-light": v(t, e, "light"), "--mantine-datatable-color-dark": v(t, e, "dark"), "--mantine-datatable-background-color-light": v(o, e, "light"), "--mantine-datatable-background-color-dark": v(o, e, "dark"), "--mantine-datatable-border-color-light": v(n, e, "light"), "--mantine-datatable-border-color-dark": v(n, e, "dark"), "--mantine-datatable-row-border-color-light": v(a, e, "light"), "--mantine-datatable-row-border-color-dark": v(a, e, "dark"), "--mantine-datatable-striped-color-light": v(r2, e, "light"), "--mantine-datatable-striped-color-dark": v(r2, e, "dark"), "--mantine-datatable-highlight-on-hover-color-light": v(l, e, "light"), "--mantine-datatable-highlight-on-hover-color-dark": v(l, e, "dark") };
}
function Xe({ theme: e, paginationActiveTextColor: t, paginationActiveBackgroundColor: o }) {
  return { "--mantine-datatable-pagination-active-text-color-light": v(t, e, "light"), "--mantine-datatable-pagination-active-text-color-dark": v(t, e, "dark"), "--mantine-datatable-pagination-active-background-color-light": v(o, e, "light"), "--mantine-datatable-pagination-active-background-color-dark": v(o, e, "dark") };
}
function go({ theme: e, color: t, backgroundColor: o }) {
  return { "--mantine-datatable-row-color-light": v(t, e, "light"), "--mantine-datatable-row-color-dark": v(t, e, "dark"), "--mantine-datatable-row-background-color-light": v(o, e, "light"), "--mantine-datatable-row-background-color-dark": v(o, e, "dark") };
}
function ho() {
  return jsxRuntimeExports.jsxs("svg", { width: "14", height: "14", viewBox: "0 0 24 24", strokeWidth: "2", stroke: "currentColor", fill: "none", strokeLinecap: "round", strokeLinejoin: "round", children: [jsxRuntimeExports.jsx("path", { stroke: "none", d: "M0 0h24v24H0z", fill: "none" }), jsxRuntimeExports.jsx("path", { d: "M8 9l4 -4l4 4" }), jsxRuntimeExports.jsx("path", { d: "M16 15l-4 4l-4 -4" })] });
}
var Do = { xs: Re(22), sm: Re(26), md: Re(32), lg: Re(38), xl: Re(44) };
function wo({ size: e, label: t, values: o, value: n, activeTextColor: a, activeBackgroundColor: r2, onChange: l }) {
  return jsxRuntimeExports.jsxs(yr, { gap: "xs", children: [jsxRuntimeExports.jsx(Co, { component: "div", size: e, children: t }), jsxRuntimeExports.jsxs(wr, { withinPortal: true, withArrow: true, classNames: { arrow: "mantine-datatable-page-size-selector-menu-arrow" }, children: [jsxRuntimeExports.jsx(xr, { children: jsxRuntimeExports.jsx(Dr, { size: e, variant: "default", classNames: { section: "mantine-datatable-page-size-selector-button-icon" }, rightSection: jsxRuntimeExports.jsx(ho, {}), style: [{ fontWeight: "normal" }, (i) => ({ height: Do[e], paddingLeft: i.spacing[e], paddingRight: i.spacing[e] })], children: n }) }), jsxRuntimeExports.jsx(Sr, { children: o.map((i) => {
    let s = i === n;
    return jsxRuntimeExports.jsx(Pr, { className: clsx({ "mantine-datatable-page-size-selector-active": s }), style: [{ height: Do[e] }, s && (a || r2) ? (d) => Xe({ theme: d, paginationActiveTextColor: a, paginationActiveBackgroundColor: r2 }) : void 0], disabled: s, onClick: () => l(i), children: jsxRuntimeExports.jsx(Co, { component: "div", size: e, children: i }) }, i);
  }) })] })] });
}
var Po = Nr(function({ className: t, style: o, fetching: n, page: a, onPageChange: r2, paginationWithEdges: l, paginationWithControls: i, paginationActiveTextColor: s, paginationActiveBackgroundColor: d, paginationSize: m, loadingText: b, noRecordsText: p, paginationText: T, totalRecords: g, recordsPerPage: x, onRecordsPerPageChange: D, recordsPerPageLabel: S, recordsPerPageOptions: R, recordsLength: P, horizontalSpacing: M, paginationWrapBreakpoint: N, getPaginationControlProps: A }, c) {
  let y;
  if (g) {
    let u = (a - 1) * x + 1, w = u + (P || 0) - 1;
    y = T({ from: u, to: w, totalRecords: g });
  } else y = n ? b : p;
  let f = K(({ breakpoints: u }) => `(min-width: ${typeof N == "number" ? `${Er(N)}rem` : u[N] || N})`);
  return jsxRuntimeExports.jsxs(Rr, { ref: c, px: M ?? "xs", py: "xs", className: clsx("mantine-datatable-pagination", t), style: [{ flexDirection: f ? "row" : "column" }, o], children: [jsxRuntimeExports.jsx(kr, { component: "div", className: "mantine-datatable-pagination-text", size: m, children: y }), R && jsxRuntimeExports.jsx(wo, { activeTextColor: s, activeBackgroundColor: d, size: m, label: S, values: R, value: x, onChange: D }), jsxRuntimeExports.jsx(Mr, { classNames: { root: clsx("mantine-datatable-pagination-pages", { "mantine-datatable-pagination-pages-fetching": n || !P }), control: "mantine-datatable-pagination-pages-control" }, style: s || d ? (u) => Xe({ theme: u, paginationActiveTextColor: s, paginationActiveBackgroundColor: d }) : void 0, withEdges: l, withControls: i, value: a, onChange: r2, size: m, total: Math.ceil(g / x), getControlProps: A })] });
});
const Gr = window["MantineCore"].TableTr;
const Hr = window["MantineCore"].TableTd;
function xo({ className: e, style: t, visibleMediaQuery: o, record: n, index: a, onClick: r2, onDoubleClick: l, onContextMenu: i, noWrap: s, ellipsis: d, textAlign: m, width: b, accessor: p, render: T, defaultRender: g, customCellAttributes: x }) {
  return K(o) ? jsxRuntimeExports.jsx(Hr, { className: clsx({ [ue]: s || d, [me]: d, [B]: r2 || l, [Ae]: i, [J]: m === "left", [Z]: m === "center", [Y]: m === "right" }, e), style: [{ width: b, minWidth: b, maxWidth: b }, t], onClick: r2, onDoubleClick: l, onContextMenu: i, ...x == null ? void 0 : x(n, a), children: T ? T(n, a) : g ? g(n, a, p) : rt(n, p) }) : null;
}
const Wr = window["MantineCore"].Collapse;
const Ar = window["MantineCore"].TableTd;
const vo = window["MantineCore"].TableTr;
function Ro({ open: e, colSpan: t, content: o, collapseProps: n }) {
  let { expanded: a, visible: r2 } = Xt(e, n == null ? void 0 : n.transitionDuration);
  return r2 ? jsxRuntimeExports.jsxs(jsxRuntimeExports.Fragment, { children: [jsxRuntimeExports.jsx(vo, {}), jsxRuntimeExports.jsx(vo, { children: jsxRuntimeExports.jsx(Ar, { className: "mantine-datatable-row-expansion-cell", colSpan: t, children: jsxRuntimeExports.jsx(Wr, { in: a, ...n, children: jsxRuntimeExports.jsx("div", { className: "mantine-datatable-row-expansion-cell-content", children: o() }) }) }) })] }) : null;
}
const _r = window["MantineCore"].Checkbox;
const Fr = window["MantineCore"].TableTd;
function ko({ className: e, style: t, record: o, index: n, trigger: a, onChange: r2, withRightShadow: l, checkboxProps: i, getCheckboxProps: s, ...d }) {
  let m = { ...i, ...s(o, n) }, b = !d.disabled && !m.disabled, p = (T) => {
    T.stopPropagation(), a === "cell" && b && (r2 == null ? void 0 : r2(T));
  };
  return jsxRuntimeExports.jsx(Fr, { className: clsx("mantine-datatable-row-selector-cell", { [B]: a === "cell" && b }, e), style: t, "data-shadow-visible": l || void 0, onClick: p, children: jsxRuntimeExports.jsx(_r, { classNames: b ? { input: B } : void 0, onChange: r2, ...d, ...m }) });
}
function Lo({ record: e, index: t, columns: o, defaultColumnProps: n, defaultColumnRender: a, selectionTrigger: r2, selectionVisible: l, selectionChecked: i, onSelectionChange: s, isRecordSelectable: d, selectionCheckboxProps: m, getSelectionCheckboxProps: b, onClick: p, onDoubleClick: T, onContextMenu: g, onCellClick: x, onCellDoubleClick: D, onCellContextMenu: S, expansion: R, customAttributes: P, color: M, backgroundColor: N, className: A, style: c, selectorCellShadowVisible: y, selectionColumnClassName: f, selectionColumnStyle: u, rowFactory: w }) {
  let h = jsxRuntimeExports.jsxs(jsxRuntimeExports.Fragment, { children: [l && jsxRuntimeExports.jsx(ko, { className: f, style: u, record: e, index: t, trigger: r2, withRightShadow: y, checked: i, disabled: !s || (d ? !d(e, t) : false), onChange: s, checkboxProps: m, getCheckboxProps: b }), o.map(({ hidden: z, hiddenContent: Q, ...F }, k) => {
    if (z || Q) return null;
    let { accessor: U, visibleMediaQuery: G, textAlign: pe, noWrap: fe, ellipsis: be, width: Te, render: ge, cellsClassName: j, cellsStyle: he, customCellAttributes: Ce } = { ...n, ...F };
    return jsxRuntimeExports.jsx(xo, { className: typeof j == "function" ? j(e, t) : j, style: he == null ? void 0 : he(e, t), visibleMediaQuery: G, record: e, index: t, onClick: x ? (X) => x({ event: X, record: e, index: t, column: F, columnIndex: k }) : void 0, onDoubleClick: D ? (X) => D({ event: X, record: e, index: t, column: F, columnIndex: k }) : void 0, onContextMenu: S ? (X) => S({ event: X, record: e, index: t, column: F, columnIndex: k }) : void 0, accessor: U, textAlign: pe, noWrap: fe, ellipsis: be, width: Te, render: ge, defaultRender: a, customCellAttributes: Ce }, U);
  })] }), L = R && jsxRuntimeExports.jsx(Ro, { colSpan: o.filter(({ hidden: z }) => !z).length + (l ? 1 : 0), open: R.isRowExpanded(e), content: R.content({ record: e, index: t }), collapseProps: R.collapseProps }), I = Qr({ record: e, index: t, selectionChecked: i, onClick: p, onDoubleClick: T, onContextMenu: g, expansion: R, customAttributes: P, color: M, backgroundColor: N, className: A, style: c });
  return w ? w({ record: e, index: t, rowProps: I, children: h, expandedElement: L }) : jsxRuntimeExports.jsxs(jsxRuntimeExports.Fragment, { children: [jsxRuntimeExports.jsx(Gr, { ...I, children: h }), L] });
}
function Qr({ record: e, index: t, selectionChecked: o, onClick: n, onDoubleClick: a, onContextMenu: r2, expansion: l, customAttributes: i, color: s, backgroundColor: d, className: m, style: b }) {
  return { className: clsx("mantine-datatable-row", { [B]: n || a || (l == null ? void 0 : l.isExpandable({ record: e, index: t })) && (l == null ? void 0 : l.expandOnClick) }, { [Ae]: r2 }, typeof m == "function" ? m(e, t) : m), "data-selected": o || void 0, onClick: (p) => {
    if (l) {
      let { isExpandable: T, isRowExpanded: g, expandOnClick: x, expandRow: D, collapseRow: S } = l;
      T({ record: e, index: t }) && x && (g(e) ? S(e) : D(e));
    }
    n == null ? void 0 : n({ event: p, record: e, index: t });
  }, onDoubleClick: a ? (p) => a({ event: p, record: e, index: t }) : void 0, onContextMenu: r2 ? (p) => r2({ event: p, record: e, index: t }) : void 0, style: [s || d ? (p) => {
    let T = s == null ? void 0 : s(e, t), g = d == null ? void 0 : d(e, t);
    return go({ theme: p, color: T, backgroundColor: g });
  } : void 0, b == null ? void 0 : b(e, t)], ...(i == null ? void 0 : i(e, t)) ?? {} };
}
const Ho = window["MantineCore"].Box;
const Ur = window["MantineCore"].ScrollArea;
const Io = window["MantineCore"].rem;
function Oo({ topShadowVisible: e, leftShadowVisible: t, leftShadowBehind: o, rightShadowVisible: n, rightShadowBehind: a, bottomShadowVisible: r2, headerHeight: l, footerHeight: i, onScrollPositionChange: s, children: d, viewportRef: m, scrollAreaProps: b }) {
  return jsxRuntimeExports.jsxs(Ur, { ...b, viewportRef: m, classNames: { root: "mantine-datatable-scroll-area", scrollbar: "mantine-datatable-scroll-area-scrollbar", thumb: "mantine-datatable-scroll-area-thumb", corner: "mantine-datatable-scroll-area-corner" }, onScrollPositionChange: s, children: [d, jsxRuntimeExports.jsx(Ho, { className: clsx("mantine-datatable-scroll-area-shadow", "mantine-datatable-scroll-area-top-shadow", { "mantine-datatable-scroll-area-shadow-visible": e }), style: { top: l ? Io(l) : 0 } }), jsxRuntimeExports.jsx("div", { className: clsx("mantine-datatable-scroll-area-shadow", "mantine-datatable-scroll-area-left-shadow", { "mantine-datatable-scroll-area-shadow-visible": t, "mantine-datatable-scroll-area-shadow-behind": o }) }), jsxRuntimeExports.jsx("div", { className: clsx("mantine-datatable-scroll-area-shadow", "mantine-datatable-scroll-area-right-shadow", { "mantine-datatable-scroll-area-shadow-visible": n, "mantine-datatable-scroll-area-shadow-behind": a }) }), jsxRuntimeExports.jsx(Ho, { className: clsx("mantine-datatable-scroll-area-shadow", "mantine-datatable-scroll-area-bottom-shadow", { "mantine-datatable-scroll-area-shadow-visible": r2 }), style: { bottom: i ? Io(i + 1) : 0 } })] });
}
function qr({ withTableBorder: e, borderRadius: t, textSelectionDisabled: o, height: n = "100%", minHeight: a, maxHeight: r2, shadow: l, verticalAlign: i = "center", fetching: s, columns: d, storeColumnsKey: m, groups: b, pinFirstColumn: p, pinLastColumn: T, defaultColumnProps: g, defaultColumnRender: x, idAccessor: D = "id", records: S, selectionTrigger: R = "checkbox", selectedRecords: P, onSelectedRecordsChange: M, selectionColumnClassName: N, selectionColumnStyle: A, isRecordSelectable: c, selectionCheckboxProps: y, allRecordsSelectionCheckboxProps: f = { "aria-label": "Select all records" }, getRecordSelectionCheckboxProps: u = (O, ee) => ({ "aria-label": `Select record ${ee + 1}` }), sortStatus: w, sortIcons: h, onSortStatusChange: L, horizontalSpacing: I, page: z, onPageChange: Q, totalRecords: F, recordsPerPage: k, onRecordsPerPageChange: U, recordsPerPageOptions: G, recordsPerPageLabel: pe = "Records per page", paginationWithEdges: fe, paginationWithControls: be, paginationActiveTextColor: Te, paginationActiveBackgroundColor: ge, paginationSize: j = "sm", paginationText: he = ({ from: O, to: ee, totalRecords: te }) => `${O} - ${ee} / ${te}`, paginationWrapBreakpoint: Ce = "sm", getPaginationControlProps: X = (O) => O === "previous" ? { "aria-label": "Previous page" } : O === "next" ? { "aria-label": "Next page" } : {}, loaderBackgroundBlur: _o, customLoader: Fo, loaderSize: Bo, loaderType: Go, loaderColor: Xo, loadingText: Qo = "...", emptyState: Uo, noRecordsText: ut = "No records", noRecordsIcon: $o, highlightOnHover: Ko, striped: Jo, noHeader: Zo, onRowClick: Yo, onRowDoubleClick: qo, onRowContextMenu: jo, onCellClick: ea, onCellDoubleClick: ta, onCellContextMenu: oa, onScroll: mt, onScrollToTop: pt, onScrollToBottom: ft, onScrollToLeft: bt, onScrollToRight: Tt, c: aa, backgroundColor: na, borderColor: ra, rowBorderColor: la, stripedColor: ia, highlightOnHoverColor: sa, rowColor: da, rowBackgroundColor: ca, rowExpansion: ua, rowClassName: ma, rowStyle: pa, customRowAttributes: fa, scrollViewportRef: ba, scrollAreaProps: Ta, tableRef: ga, bodyRef: ha, m: Ca, my: Da, mx: ya, mt: wa, mb: Sa, ml: Pa, mr: xa, className: va, classNames: De, style: Ra, styles: ye, rowFactory: Ma, tableWrapper: Je, ...gt }) {
  let { ref: O, width: ee, height: te } = ne(), we = Yr(() => (b == null ? void 0 : b.flatMap((C) => C.columns)) ?? d, [d, b]), ht = It({ key: m, columns: we }), { ref: ka, height: Ze } = ne(), { ref: Ea, width: Ye, height: Se } = ne(), { ref: Na, height: La } = ne(), { ref: Ha, height: Ct } = ne(), { ref: Ia, width: Oa } = ne(), Wa = useMergedRef(Ea, ga), Aa = useMergedRef(O, ba), [qe, Dt] = Ke(true), [je, yt] = Ke(true), [Pe, wt] = Ke(true), [Ee, St] = Ke(true), za = Ft({ rowExpansion: ua, records: S, idAccessor: D }), et = ke(() => {
    var _a3, _b2;
    let C = ((_a3 = O.current) == null ? void 0 : _a3.scrollTop) ?? 0, $ = ((_b2 = O.current) == null ? void 0 : _b2.scrollLeft) ?? 0;
    if (s || Se <= te) Dt(true), yt(true);
    else {
      let V = C === 0, _ = Se - C - te < 1;
      Dt(V), yt(_), V && V !== qe && (pt == null ? void 0 : pt()), _ && _ !== je && (ft == null ? void 0 : ft());
    }
    if (s || Ye === ee) wt(true), St(true);
    else {
      let V = $ === 0, _ = Ye - $ - ee < 1;
      wt(V), St(_), V && V !== Pe && (bt == null ? void 0 : bt()), _ && _ !== Ee && (Tt == null ? void 0 : Tt());
    }
  }, [s, ft, bt, Tt, pt, te, O, ee, je, Pe, Ee, qe, Se, Ye]);
  Ot(et, [et]);
  let Pt = useDebouncedCallback(et, 50), Va = ke((C) => {
    mt == null ? void 0 : mt(C), Pt();
  }, [Pt, mt]), _a2 = ke((C) => {
    var _a3;
    (_a3 = O.current) == null ? void 0 : _a3.scrollTo({ top: 0, left: 0 }), Q(C);
  }, [Q, O]), Ne = S == null ? void 0 : S.length, xt = S == null ? void 0 : S.map((C) => E(C, D)), ie = !!P, xe = P == null ? void 0 : P.map((C) => E(C, D)), vt = xt !== void 0 && xe !== void 0 && xe.length > 0, tt = c ? S == null ? void 0 : S.filter(c) : S, Le = tt == null ? void 0 : tt.map((C) => E(C, D)), He = vt && Le.every((C) => xe.includes(C)), Fa = vt && Le.some((C) => xe.includes(C)), Ba = ke(() => {
    P && M && M(He ? P.filter((C) => !Le.includes(E(C, D))) : We([...P, ...tt], (C) => E(C, D)));
  }, [He, D, M, Le, tt, P]), { lastSelectionChangeIndex: Ie, setLastSelectionChangeIndex: Ga } = Wt(xt), ot = ie && !Pe && !p, Xa = { m: Ca, my: Da, mx: ya, mt: wa, mb: Sa, ml: Pa, mr: xa }, Qa = ke(({ children: C }) => Je ? Je({ children: C }) : C, [Je]);
  return jsxRuntimeExports.jsx(at, { ...ht, children: jsxRuntimeExports.jsxs(Kr, { ...Xa, className: clsx("mantine-datatable", { "mantine-datatable-with-border": e }, va, De == null ? void 0 : De.root), style: [(C) => ({ ...To({ theme: C, c: aa, backgroundColor: na, borderColor: ra, rowBorderColor: la, stripedColor: ia, highlightOnHoverColor: sa }), borderRadius: C.radius[t] || t, boxShadow: C.shadows[l] || l, height: n, minHeight: a, maxHeight: r2 }), Ra, ye == null ? void 0 : ye.root, { position: "relative" }], children: [jsxRuntimeExports.jsx(Oo, { viewportRef: Aa, topShadowVisible: !qe, leftShadowVisible: !Pe, leftShadowBehind: ie || !!p, rightShadowVisible: !Ee, rightShadowBehind: T, bottomShadowVisible: !je, headerHeight: Ze, footerHeight: La, onScrollPositionChange: Va, scrollAreaProps: Ta, children: jsxRuntimeExports.jsx(Qa, { children: jsxRuntimeExports.jsxs(Jr, { ref: Wa, horizontalSpacing: I, className: clsx("mantine-datatable-table", { [Qt]: o, "mantine-datatable-vertical-align-top": i === "top", "mantine-datatable-vertical-align-bottom": i === "bottom", "mantine-datatable-last-row-border-bottom-visible": gt.withRowBorders && Se < te, "mantine-datatable-pin-last-column": T, "mantine-datatable-pin-last-column-scrolled": !Ee && T, "mantine-datatable-selection-column-visible": ie, "mantine-datatable-pin-first-column": p, "mantine-datatable-pin-first-column-scrolled": !Pe && p }, De == null ? void 0 : De.table), style: { ...ye == null ? void 0 : ye.table, "--mantine-datatable-selection-column-width": `${Oa}px` }, "data-striped": Ne && Jo || void 0, "data-highlight-on-hover": Ko || void 0, ...gt, children: [Zo ? null : jsxRuntimeExports.jsx(at, { ...ht, children: jsxRuntimeExports.jsx(po, { ref: ka, selectionColumnHeaderRef: Ia, className: De == null ? void 0 : De.header, style: ye == null ? void 0 : ye.header, columns: we, defaultColumnProps: g, groups: b, sortStatus: w, sortIcons: h, onSortStatusChange: L, selectionTrigger: R, selectionVisible: ie, selectionChecked: He, selectionIndeterminate: Fa && !He, onSelectionChange: Ba, selectionCheckboxProps: { ...y, ...f }, selectorCellShadowVisible: ot, selectionColumnClassName: N, selectionColumnStyle: A }) }), jsxRuntimeExports.jsx("tbody", { ref: ha, children: Ne ? S.map((C, $) => {
    let V = E(C, D), _ = (xe == null ? void 0 : xe.includes(V)) || false, Rt;
    return M && P && (Rt = (Ua) => {
      if (Ua.nativeEvent.shiftKey && Ie !== null) {
        let se = S.filter($ > Ie ? (oe, ae) => ae >= Ie && ae <= $ && (c ? c(oe, ae) : true) : (oe, ae) => ae >= $ && ae <= Ie && (c ? c(oe, ae) : true));
        M(_ ? _t(P, se, (oe) => E(oe, D)) : We([...P, ...se], (oe) => E(oe, D)));
      } else M(_ ? P.filter((se) => E(se, D) !== V) : We([...P, C], (se) => E(se, D)));
      Ga($);
    }), jsxRuntimeExports.jsx(Lo, { record: C, index: $, columns: we, defaultColumnProps: g, defaultColumnRender: x, selectionTrigger: R, selectionVisible: ie, selectionChecked: _, onSelectionChange: Rt, isRecordSelectable: c, selectionCheckboxProps: y, getSelectionCheckboxProps: u, onClick: Yo, onDoubleClick: qo, onCellClick: ea, onCellDoubleClick: ta, onContextMenu: jo, onCellContextMenu: oa, expansion: za, color: da, backgroundColor: ca, className: ma, style: pa, customAttributes: fa, selectorCellShadowVisible: ot, selectionColumnClassName: N, selectionColumnStyle: A, idAccessor: D, rowFactory: Ma }, V);
  }) : jsxRuntimeExports.jsx(Nt, {}) }), we.some(({ footer: C }) => C) && jsxRuntimeExports.jsx(Kt, { ref: Na, className: De == null ? void 0 : De.footer, style: ye == null ? void 0 : ye.footer, columns: we, defaultColumnProps: g, selectionVisible: ie, selectorCellShadowVisible: ot, scrollDiff: Se - te })] }) }) }), z && jsxRuntimeExports.jsx(Po, { ref: Ha, className: De == null ? void 0 : De.pagination, style: ye == null ? void 0 : ye.pagination, horizontalSpacing: I, fetching: s, page: z, onPageChange: _a2, totalRecords: F, recordsPerPage: k, onRecordsPerPageChange: U, recordsPerPageOptions: G, recordsPerPageLabel: pe, paginationWithEdges: fe, paginationWithControls: be, paginationActiveTextColor: Te, paginationActiveBackgroundColor: ge, paginationSize: j, paginationText: he, paginationWrapBreakpoint: Ce, getPaginationControlProps: X, noRecordsText: ut, loadingText: Qo, recordsLength: Ne }), jsxRuntimeExports.jsx(bo, { pt: Ze, pb: Ct, fetching: s, backgroundBlur: _o, customContent: Fo, size: Bo, type: Go, color: Xo }), jsxRuntimeExports.jsx(Ht, { pt: Ze, pb: Ct, icon: $o, text: ut, active: !s && !Ne, children: Uo })] }) });
}
const jr = window["MantineCore"].TableTr;
const tl = window["React"].forwardRef;
const ol = window["React"].useEffect;
const al = window["React"].useRef;
var Vo = tl(function({ children: e, isDragging: t, ...o }, n) {
  let a = al(null), r2 = useMergedRef(a, n);
  return ol(() => {
    if (!a.current || !t) return;
    let d = a.current.parentElement.parentElement.children[0].children[0];
    for (let m = 0; m < d.children.length; m++) {
      let p = d.children[m].getBoundingClientRect(), T = a.current.children[m];
      T.style.height = p.height + "px", T.style.width = p.width + "px", T.style.minWidth = p.width + "px", T.style.maxWidth = p.width + "px";
    }
  }, [t, e]), jsxRuntimeExports.jsx(jr, { "data-is-dragging": t, ref: r2, ...o, children: e });
});
Vo.displayName = "DataTableDraggableRow";
export {
  AddItemButton as A,
  IconInfoCircle as I,
  RowEditAction as R,
  SearchInput as S,
  apiUrl as a,
  RowDuplicateAction as b,
  RowDeleteAction as c,
  RowActions as d,
  IconExclamationCircle as e,
  formatCurrencyValue as f,
  IconRefresh as g,
  checkPluginVersion as h,
  createReactComponent as i,
  formatDecimal as j,
  qr as q,
  useQuery as u
};
//# sourceMappingURL=index-BjwOiYns.js.map
