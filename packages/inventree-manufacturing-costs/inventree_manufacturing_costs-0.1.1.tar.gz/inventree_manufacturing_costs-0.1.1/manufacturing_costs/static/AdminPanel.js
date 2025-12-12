import { u as useQuery, a as apiUrl, R as RowEditAction, b as RowDuplicateAction, c as RowDeleteAction, f as formatCurrencyValue, d as RowActions, I as IconInfoCircle, e as IconExclamationCircle, A as AddItemButton, S as SearchInput, g as IconRefresh, q as qr, h as checkPluginVersion } from "./assets/index-BjwOiYns.js";
const ActionIcon = window["MantineCore"].ActionIcon;
const Alert = window["MantineCore"].Alert;
const Group = window["MantineCore"].Group;
const Stack = window["MantineCore"].Stack;
const Text = window["MantineCore"].Text;
const Tooltip = window["MantineCore"].Tooltip;
const useCallback = window["React"].useCallback;
const useMemo = window["React"].useMemo;
const useState = window["React"].useState;
function ManufacturingCostsAdminPanel({
  context
}) {
  const [searchTerm, setSearchTerm] = useState("");
  const RATE_URL = "/plugin/manufacturing-costs/rate/";
  const dataQuery = useQuery(
    {
      queryKey: ["manufacturing-rate", searchTerm],
      queryFn: async () => {
        var _a;
        return (_a = context == null ? void 0 : context.api) == null ? void 0 : _a.get(RATE_URL, {
          params: {
            search: searchTerm
          }
        }).then((response) => response.data);
      }
    },
    context.queryClient
  );
  const rateFields = useMemo(() => {
    return {
      name: {},
      description: {},
      price: {},
      price_currency: {},
      units: {}
    };
  }, []);
  const [selectedRecord, setSelectedRecord] = useState(null);
  const createRateForm = context.forms.create({
    url: apiUrl(RATE_URL),
    title: "Add Rate",
    fields: rateFields,
    successMessage: "Rate created",
    onFormSuccess: () => {
      dataQuery.refetch();
    }
  });
  const editRateForm = context.forms.edit({
    url: apiUrl(RATE_URL, selectedRecord == null ? void 0 : selectedRecord.pk),
    title: "Edit Rate",
    fields: rateFields,
    successMessage: "Rate updated",
    onFormSuccess: () => {
      dataQuery.refetch();
    }
  });
  const deleteRateForm = context.forms.delete({
    url: apiUrl(RATE_URL, selectedRecord == null ? void 0 : selectedRecord.pk),
    title: "Delete Rate",
    successMessage: "Rate deleted",
    onFormSuccess: () => {
      dataQuery.refetch();
    }
  });
  const duplicateRateForm = context.forms.create({
    url: apiUrl(RATE_URL),
    title: "Add Rate",
    fields: rateFields,
    initialData: {
      ...selectedRecord
    },
    successMessage: "Rate created",
    onFormSuccess: () => {
      dataQuery.refetch();
    }
  });
  const rowActions = useCallback((record) => {
    return [
      RowEditAction({
        onClick: () => {
          setSelectedRecord(record);
          editRateForm == null ? void 0 : editRateForm.open();
        }
      }),
      RowDuplicateAction({
        onClick: () => {
          setSelectedRecord(record);
          duplicateRateForm == null ? void 0 : duplicateRateForm.open();
        }
      }),
      RowDeleteAction({
        onClick: () => {
          setSelectedRecord(record);
          deleteRateForm == null ? void 0 : deleteRateForm.open();
        }
      })
    ];
  }, []);
  const dataColumns = useMemo(() => {
    return [
      {
        accessor: "name",
        sortable: true
      },
      {
        accessor: "description"
      },
      {
        accessor: "price",
        title: "Rate",
        sortable: true,
        render: (record) => {
          return /* @__PURE__ */ React.createElement(Group, { gap: "sm" }, /* @__PURE__ */ React.createElement(Text, null, formatCurrencyValue(record.price, {
            currency: record.price_currency
          })), record.units && /* @__PURE__ */ React.createElement(Text, { size: "xs" }, "[", record.units, "]"));
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
  return /* @__PURE__ */ React.createElement(React.Fragment, null, createRateForm == null ? void 0 : createRateForm.modal, editRateForm == null ? void 0 : editRateForm.modal, duplicateRateForm == null ? void 0 : duplicateRateForm.modal, deleteRateForm == null ? void 0 : deleteRateForm.modal, /* @__PURE__ */ React.createElement(Stack, { gap: "xs" }, /* @__PURE__ */ React.createElement(
    Alert,
    {
      color: "blue",
      icon: /* @__PURE__ */ React.createElement(IconInfoCircle, null),
      title: "Manufacturing Rates"
    },
    "Predefined rates for different manufaucturing processes. These can be referenced to assign manufaucturing costs to parts."
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
        createRateForm == null ? void 0 : createRateForm.open();
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
  )))), /* @__PURE__ */ React.createElement(
    qr,
    {
      minHeight: 250,
      withTableBorder: true,
      withColumnBorders: true,
      idAccessor: "pk",
      noRecordsText: "No manufacturing rates found",
      records: dataQuery.data || [],
      fetching: dataQuery.isFetching || dataQuery.isLoading,
      columns: dataColumns,
      pinLastColumn: true
    }
  )));
}
function renderAdminPanel(context) {
  checkPluginVersion(context);
  return /* @__PURE__ */ React.createElement(ManufacturingCostsAdminPanel, { context });
}
export {
  ManufacturingCostsAdminPanel,
  renderAdminPanel
};
//# sourceMappingURL=AdminPanel.js.map
