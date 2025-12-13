const SELECT_MAP_ID_POSTFIX = "-select";

class MapCompositionBlockDefinition extends window.wagtailStreamField.blocks.FieldBlockDefinition {
    slimSelects = {};

    render(placeholder, prefix, initialState, initialError) {
        const block = super.render(placeholder, prefix, initialState, initialError);
      const selectField = document.getElementById(prefix + SELECT_MAP_ID_POSTFIX);

        this.slimSelects[prefix] = new SlimSelect({
            select: selectField,
            allowDeselect: true,
            showOptionTooltips: true,
            onChange: this.onSelectionChange,
            addable: this.onValueAdded,
            searchPlaceholder: 'Search or enter URL'
        });

        fetch(this.getLaymanBaseUrl() + "/layman-proxy/rest/maps")
            .then(response => response.json())
            .then(data => this.handleLaymanMaps(data, prefix))
            .catch(error => {
                console.error(error);
                this.handleLaymanMaps([], prefix);
            });

        return block;
    }

    getLaymanBaseUrl() {
        let origin = window.location.origin;
        if (origin.includes("localhost" | "127.0.0.1")) {
            console.warn("If you want to load Layman map compositions from local/development enviroment use local-cors-proxy (https://github.com/garmeeh/local-cors-proxy) to overcome CORS issues.");

            return origin.substring(0, origin.lastIndexOf(':') + 1) + LOCAL_LAYMAN_PORT;
        }

        return origin;
    }

    handleLaymanMaps(maps, inputId) {
        let inputValue = document.getElementById(inputId).value;
        let hasValueFromLayman = false;

        let options = maps.map(map => {
            let option = {
                text: map.title,
                value: map.url
            }

            if (map.url === inputValue) {
                hasValueFromLayman = true;
                option.selected = true;
            }

            return option;
        });

        if (!hasValueFromLayman && inputValue !== '') {
            options.unshift({
                text: inputValue,
                value: inputValue,
                selected: true,
            })
        }

        options.unshift({
            text: "Select or add map composition",
            placeholder: true
        })

        this.slimSelects[inputId].setData(options);
  }

    onValueAdded(value) {
        return value;
    }

    onSelectionChange(selectedOption) {
      let selectId = this.select.element.id;
      let selectInputId = selectId.substring(0, selectId.lastIndexOf(SELECT_MAP_ID_POSTFIX));
      let input = document.getElementById(selectInputId);
        input.value = selectedOption.value === "undefined" ? "" : selectedOption.value;

      let url = PROXY_URL + selectedOption.value;
      if (url.substring(url.length - 5, url.length) != "/file")
        url += "/file";
      fetch(url)
        .then(response => response.json())
        .then(data => {
          let mapCenterElement = document.getElementById(selectInputId.replace("composition_url", "map_center"));
          if (mapCenterElement && data.center) {
            mapCenterElement.value = `${data.center[0]}, ${data.center[1]}`;

            let zoomElement = document.getElementById(selectInputId.replace("composition_url", "map_zoom"));
            if (zoomElement)
              zoomElement.value = getBoundsZoomLevel(data.extent, { width: 1024, height: 960 });
          }

          let crsId = selectInputId.replace("composition_url", "settings-projection");
          let crsElement = document.getElementById(crsId);
          let crsSelect = document.getElementById(crsId + "-select");
          if (crsElement && data.projection) {
            let crs = data.projection.toUpperCase();
            crsElement.value = crs;

            crsSelect.slim.setData([{ text: crs, value: crs }]);
            crsSelect.slim.setSelected(crs);
          }
        })
        .catch(error => {
          console.error(error);
          this.handleSelectedMap([], selectInputId);
        });
  }
}

window.telepath.register('hslayers.blocks.MapCompositionBlock', MapCompositionBlockDefinition);