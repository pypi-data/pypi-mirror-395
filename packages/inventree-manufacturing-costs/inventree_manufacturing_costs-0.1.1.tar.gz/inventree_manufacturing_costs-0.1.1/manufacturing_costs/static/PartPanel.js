import { i as createReactComponent, h as checkPluginVersion, a as apiUrl, u as useQuery, R as RowEditAction, b as RowDuplicateAction, c as RowDeleteAction, j as formatDecimal, f as formatCurrencyValue, I as IconInfoCircle, d as RowActions, e as IconExclamationCircle, A as AddItemButton, S as SearchInput, g as IconRefresh, q as qr } from "./assets/index-BjwOiYns.js";
var ModelType = /* @__PURE__ */ ((ModelType2) => {
  ModelType2["part"] = "part";
  ModelType2["supplierpart"] = "supplierpart";
  ModelType2["manufacturerpart"] = "manufacturerpart";
  ModelType2["partcategory"] = "partcategory";
  ModelType2["partparametertemplate"] = "partparametertemplate";
  ModelType2["parttesttemplate"] = "parttesttemplate";
  ModelType2["projectcode"] = "projectcode";
  ModelType2["stockitem"] = "stockitem";
  ModelType2["stocklocation"] = "stocklocation";
  ModelType2["stocklocationtype"] = "stocklocationtype";
  ModelType2["stockhistory"] = "stockhistory";
  ModelType2["build"] = "build";
  ModelType2["buildline"] = "buildline";
  ModelType2["builditem"] = "builditem";
  ModelType2["company"] = "company";
  ModelType2["purchaseorder"] = "purchaseorder";
  ModelType2["purchaseorderlineitem"] = "purchaseorderlineitem";
  ModelType2["salesorder"] = "salesorder";
  ModelType2["salesordershipment"] = "salesordershipment";
  ModelType2["returnorder"] = "returnorder";
  ModelType2["returnorderlineitem"] = "returnorderlineitem";
  ModelType2["importsession"] = "importsession";
  ModelType2["address"] = "address";
  ModelType2["contact"] = "contact";
  ModelType2["owner"] = "owner";
  ModelType2["user"] = "user";
  ModelType2["group"] = "group";
  ModelType2["reporttemplate"] = "reporttemplate";
  ModelType2["labeltemplate"] = "labeltemplate";
  ModelType2["pluginconfig"] = "pluginconfig";
  ModelType2["contenttype"] = "contenttype";
  ModelType2["selectionlist"] = "selectionlist";
  ModelType2["error"] = "error";
  return ModelType2;
})(ModelType || {});
/**
 * @license @tabler/icons-react v3.34.1 - MIT
 *
 * This source code is licensed under the MIT license.
 * See the LICENSE file in the root directory of this source tree.
 */
const __iconNode$1 = [["path", { "d": "M14 3v4a1 1 0 0 0 1 1h4", "key": "svg-0" }], ["path", { "d": "M17 21h-10a2 2 0 0 1 -2 -2v-14a2 2 0 0 1 2 -2h7l5 5v11a2 2 0 0 1 -2 2z", "key": "svg-1" }], ["path", { "d": "M12 17v-6", "key": "svg-2" }], ["path", { "d": "M9.5 14.5l2.5 2.5l2.5 -2.5", "key": "svg-3" }]];
const IconFileDownload = createReactComponent("outline", "file-download", "FileDownload", __iconNode$1);
/**
 * @license @tabler/icons-react v3.34.1 - MIT
 *
 * This source code is licensed under the MIT license.
 * See the LICENSE file in the root directory of this source tree.
 */
const __iconNode = [["path", { "d": "M8 7a4 4 0 1 0 8 0a4 4 0 0 0 -8 0", "key": "svg-0" }], ["path", { "d": "M6 21v-2a4 4 0 0 1 4 -4h4a4 4 0 0 1 4 4v2", "key": "svg-1" }]];
const IconUser = createReactComponent("outline", "user", "User", __iconNode);
const ActionIcon = window["MantineCore"].ActionIcon;
const Alert = window["MantineCore"].Alert;
const Button = window["MantineCore"].Button;
const Group = window["MantineCore"].Group;
const HoverCard = window["MantineCore"].HoverCard;
const Menu = window["MantineCore"].Menu;
const Stack = window["MantineCore"].Stack;
const Text = window["MantineCore"].Text;
const Tooltip = window["MantineCore"].Tooltip;
const useCallback = window["React"].useCallback;
const useMemo = window["React"].useMemo;
const useState = window["React"].useState;
function RenderRate({ instance }) {
  return /* @__PURE__ */ React.createElement(Group, { gap: "xs", justify: "space-between" }, /* @__PURE__ */ React.createElement(Text, null, instance.name), /* @__PURE__ */ React.createElement(Group, { gap: "xs", justify: "right" }, /* @__PURE__ */ React.createElement(Text, { size: "xs" }, instance.description), instance.units && /* @__PURE__ */ React.createElement(Text, { size: "xs" }, "[", instance.units, "]")));
}
function ManufacturingCostsPanel({
  context
}) {
  const partId = useMemo(() => {
    return context.model == ModelType.part ? context.id || null : null;
  }, [context.model, context.id]);
  const [searchTerm, setSearchTerm] = useState("");
  const RATE_URL = "/plugin/manufacturing-costs/rate/";
  const COST_URL = "/plugin/manufacturing-costs/cost/";
  const EXPORT_URL = "/plugin/manufacturing-costs/cost/export/";
  const downloadData = useCallback(
    (exportFormat) => {
      if (!partId) {
        return;
      }
      let url = `${apiUrl(EXPORT_URL)}?part=${partId}&export_format=${exportFormat}`;
      if (context.host) {
        url = `${context.host}${url}`;
      } else {
        url = `${window.location.origin}${url}`;
      }
      window.open(url, "_blank");
    },
    [partId, context.host, window.location]
  );
  const dataQuery = useQuery(
    {
      queryKey: ["manufacturing-cost", partId, searchTerm],
      queryFn: async () => {
        var _a;
        const url = `${COST_URL}`;
        return ((_a = context.api) == null ? void 0 : _a.get(url, {
          params: {
            part: partId,
            search: searchTerm
          }
        }).then((response) => response.data).catch(() => [])) ?? [];
      }
    },
    context.queryClient
  );
  const [selectedRecord, setSelectedRecord] = useState(null);
  const costFields = useMemo(() => {
    return {
      part: {
        value: partId,
        disabled: true
      },
      description: {},
      quantity: {},
      // TODO: Add a "pre-field" element here
      rate: {
        api_url: apiUrl(RATE_URL),
        modelRenderer: RenderRate
      },
      // TODO: Mark unit_cost and unit_cost currency as "disabled" if a rate is selected
      unit_cost: {},
      unit_cost_currency: {},
      notes: {},
      inherited: {},
      active: {}
    };
  }, []);
  const createCostForm = context.forms.create({
    url: apiUrl(COST_URL),
    title: "Add Manufacturing Cost",
    fields: costFields,
    successMessage: "Cost created",
    onFormSuccess: () => {
      dataQuery.refetch();
    }
  });
  const duplicateCostForm = context.forms.create({
    url: apiUrl(COST_URL),
    title: "Add Manufacturing Cost",
    fields: costFields,
    successMessage: "Cost created",
    initialData: selectedRecord,
    onFormSuccess: () => {
      dataQuery.refetch();
    }
  });
  const editCostForm = context.forms.edit({
    url: apiUrl(COST_URL, selectedRecord == null ? void 0 : selectedRecord.pk),
    title: "Edit Manufacturing Cost",
    fields: costFields,
    successMessage: "Cost updated",
    onFormSuccess: () => {
      dataQuery.refetch();
    }
  });
  const deleteCostForm = context.forms.delete({
    url: apiUrl(COST_URL, selectedRecord == null ? void 0 : selectedRecord.pk),
    title: "Delete Manufacturing Cost",
    successMessage: "Cost deleted",
    onFormSuccess: () => {
      dataQuery.refetch();
    }
  });
  const rowActions = useCallback(
    (record) => {
      const partPk = context.instance.pk;
      return [
        RowEditAction({
          onClick: () => {
            setSelectedRecord(record);
            editCostForm == null ? void 0 : editCostForm.open();
          },
          hidden: record.part != partPk
        }),
        RowDuplicateAction({
          onClick: () => {
            setSelectedRecord(record);
            duplicateCostForm == null ? void 0 : duplicateCostForm.open();
          }
        }),
        RowDeleteAction({
          onClick: () => {
            setSelectedRecord(record);
            deleteCostForm == null ? void 0 : deleteCostForm.open();
          },
          hidden: record.part != partPk
        })
      ];
    },
    [context.instance]
  );
  const tableColums = useMemo(() => {
    return [
      {
        accessor: "part",
        title: "Part",
        render: (record) => {
          var _a;
          return (_a = record.part_detail) == null ? void 0 : _a.full_name;
        }
      },
      {
        accessor: "part_detail.IPN",
        title: "IPN"
      },
      {
        accessor: "description",
        title: "Description"
      },
      {
        accessor: "quantity",
        title: "Quantity",
        format: (value) => formatDecimal(value)
      },
      {
        accessor: "rate",
        title: "Rate",
        render: (record) => {
          const rate = record.rate_detail;
          let unit_cost = "";
          if (rate) {
            unit_cost = formatCurrencyValue(rate.price, {
              currency: rate.price_currency
            });
          } else {
            unit_cost = formatCurrencyValue(record.unit_cost, {
              currency: record.unit_cost_currency
            });
          }
          return /* @__PURE__ */ React.createElement(Group, { justify: "space-between", gap: "sm" }, /* @__PURE__ */ React.createElement(Text, null, unit_cost), rate && /* @__PURE__ */ React.createElement(HoverCard, null, /* @__PURE__ */ React.createElement(HoverCard.Target, null, /* @__PURE__ */ React.createElement(ActionIcon, { variant: "transparent", size: "sm" }, /* @__PURE__ */ React.createElement(IconInfoCircle, null))), /* @__PURE__ */ React.createElement(HoverCard.Dropdown, null, /* @__PURE__ */ React.createElement(RenderRate, { instance: rate }))));
        }
      },
      {
        accessor: "notes",
        title: "Notes"
      },
      {
        accessor: "inherited",
        title: "Inherited",
        render: (record) => record.inherited ? "Yes" : "No"
      },
      {
        accessor: "active",
        title: "Active",
        render: (record) => record.active ? "Yes" : "No"
      },
      {
        accessor: "updated",
        title: "Updated",
        render: (record) => {
          return /* @__PURE__ */ React.createElement(Group, { justify: "space-between" }, /* @__PURE__ */ React.createElement(Text, null, record.updated), record.updated_by_detail && /* @__PURE__ */ React.createElement(HoverCard, { position: "bottom-end" }, /* @__PURE__ */ React.createElement(HoverCard.Target, null, /* @__PURE__ */ React.createElement(ActionIcon, { variant: "transparent", size: "sm" }, /* @__PURE__ */ React.createElement(IconUser, null))), /* @__PURE__ */ React.createElement(HoverCard.Dropdown, null, context.renderInstance({
            model: ModelType.user,
            instance: record.updated_by_detail
          }))));
        }
      },
      {
        accessor: "---",
        title: " ",
        width: 50,
        resizable: false,
        sortable: false,
        render: (record, index) => /* @__PURE__ */ React.createElement(RowActions, { actions: rowActions(record), index })
      }
    ];
  }, []);
  return /* @__PURE__ */ React.createElement(React.Fragment, null, createCostForm.modal, duplicateCostForm.modal, editCostForm.modal, deleteCostForm.modal, /* @__PURE__ */ React.createElement(Stack, { gap: "xs" }, /* @__PURE__ */ React.createElement(
    Alert,
    {
      color: "blue",
      icon: /* @__PURE__ */ React.createElement(IconInfoCircle, null),
      title: "Manufacturing Costs"
    },
    "Additional manufacturing costs associated with this assembly."
  ), dataQuery.isError && /* @__PURE__ */ React.createElement(
    Alert,
    {
      color: "red",
      title: "Error Fetching Data",
      icon: /* @__PURE__ */ React.createElement(IconExclamationCircle, null)
    },
    dataQuery.error instanceof Error ? dataQuery.error.message : "An error occurred while fetching data from the server."
  ), /* @__PURE__ */ React.createElement(Group, { justify: "space-between" }, /* @__PURE__ */ React.createElement(Group, { gap: "xs" }, /* @__PURE__ */ React.createElement(
    AddItemButton,
    {
      tooltip: "Add new rate",
      onClick: () => {
        createCostForm.open();
      }
    }
  )), /* @__PURE__ */ React.createElement(Group, { gap: "xs" }, /* @__PURE__ */ React.createElement(
    SearchInput,
    {
      searchCallback: (value) => {
        setSearchTerm(value);
      }
    }
  ), /* @__PURE__ */ React.createElement(Tooltip, { label: "Refresh data", position: "top-end" }, /* @__PURE__ */ React.createElement(
    ActionIcon,
    {
      variant: "transparent",
      onClick: () => {
        dataQuery.refetch();
      }
    },
    /* @__PURE__ */ React.createElement(IconRefresh, null)
  )), /* @__PURE__ */ React.createElement(Menu, null, /* @__PURE__ */ React.createElement(Menu.Target, null, /* @__PURE__ */ React.createElement(Button, { leftSection: /* @__PURE__ */ React.createElement(IconFileDownload, null) }, "Export")), /* @__PURE__ */ React.createElement(Menu.Dropdown, null, /* @__PURE__ */ React.createElement(Menu.Item, { onClick: () => downloadData("csv") }, "CSV"), /* @__PURE__ */ React.createElement(Menu.Item, { onClick: () => downloadData("xls") }, "XLS"), /* @__PURE__ */ React.createElement(Menu.Item, { onClick: () => downloadData("xlsx") }, "XLSX"))))), /* @__PURE__ */ React.createElement(
    qr,
    {
      minHeight: 250,
      withTableBorder: true,
      withColumnBorders: true,
      idAccessor: "pk",
      noRecordsText: "No manufacturing costs found",
      fetching: dataQuery.isFetching || dataQuery.isLoading,
      columns: tableColums,
      records: dataQuery.data || [],
      pinLastColumn: true
    }
  )));
}
function renderPartPanel(context) {
  checkPluginVersion(context);
  return /* @__PURE__ */ React.createElement(ManufacturingCostsPanel, { context });
}
export {
  renderPartPanel
};
//# sourceMappingURL=PartPanel.js.map
