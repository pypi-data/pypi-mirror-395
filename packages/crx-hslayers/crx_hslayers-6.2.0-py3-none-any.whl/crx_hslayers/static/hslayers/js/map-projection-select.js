const EPSG_API_BASE_URL =
  "https://apps.epsg.org/api/v1/CoordRefSystem/?keywords=";
const SELECT_PROJ_ID_POSTFIX = "-select";

class MapProjectionBlockDefinition extends window.wagtailStreamField.blocks
  .FieldBlockDefinition {
  slimSelects = {};

  render(placeholder, prefix, initialState, initialError) {
    const block = super.render(placeholder, prefix, initialState, initialError);
    const selectField = document.getElementById(
      prefix + SELECT_PROJ_ID_POSTFIX
    );

    this.slimSelects[prefix] = new SlimSelect({
      select: selectField,
      allowDeselect: true,
      showOptionTooltips: true,
      onChange: this.onSelectionChange,
      ajax: function (search, callback) {
        if (search.length < 3) {
          callback("At least 3 charactes are needed to search...");
          return;
        }

        let url = PROXY_URL + EPSG_API_BASE_URL + search;
        fetch(url, {
          headers: {
            Accept: "application/json",
          },
        })
          .then((response) => response.json())
          .then((data) => {
            let selectItems = data.Results.map((item) => {
              let option = {
                text: `${item.Name} (${item.DataSource}:${item.Code})`,
                value: `${item.DataSource}:${item.Code}`,
              };

              return option;
            });

            callback(selectItems);
          })
          .catch((error) => {
            console.error(error);
          });
      },
      searchPlaceholder: "Search CRS",
    });
    if (initialState && initialState != "") {
      this.slimSelects[prefix].setData([{ text: initialState, value: initialState }]);
      this.slimSelects[prefix].setSelected(initialState);
    }

    return block;
  }

  onSelectionChange(selectedOption) {
    let selectId = this.select.element.id;
    let input = document.getElementById(selectId.substring(0, selectId.lastIndexOf(SELECT_PROJ_ID_POSTFIX)));
    input.value = selectedOption.value === "undefined" ? "" : selectedOption.value;
  }
}

window.telepath.register(
  "hslayers.blocks.MapProjectionBlock",
  MapProjectionBlockDefinition
);
