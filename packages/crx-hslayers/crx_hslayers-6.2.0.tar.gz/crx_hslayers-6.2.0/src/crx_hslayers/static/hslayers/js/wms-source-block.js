class WmsSourceBlockDefiniton extends window.wagtailStreamField.blocks.StructBlockDefinition {

    constructor(blockName, childBlocks, meta, custom) {
        console.log(blockName);
        console.log(childBlocks);
        console.log(meta);
        console.log(custom);

        super(blockName, childBlocks, meta);
    }

    async render(placeholder, prefix, initialState, initialError) {
        const block = super.render(placeholder, prefix, initialState, initialError);

        const loadButton = document.getElementById(prefix + "-load");        
        const urlInput = document.getElementById(prefix + '-url');
        
        if(urlInput.value){
            await this.loadWmsLayers(prefix, loadButton);
        }

        $(loadButton).on("click", (evt) => this.loadWmsLayers(prefix, loadButton));
        
        return block;
    }

    async loadWmsLayers(prefix, loadButton){
        let urlInput = document.getElementById(prefix + '-url');
        let layerSelectorContainer = document.getElementById(prefix + '-layer-selector-container');
        let layersInput = document.getElementById(prefix + "-layers");

        this.toggleLoadButton(loadButton);
      try {
        let data = await this.getCapabilities((window.location.origin.indexOf("localhost") > -1 ? "http://localhost:8085/" : window.location.origin + '/proxy/') + urlInput.value);
            let layers = this.getLayers(data);
            this.renderLayerSelector(layers, layerSelectorContainer);

            let layerCheckboxes = $(layerSelectorContainer).find("input[type='checkbox']");

            if(layersInput.value){
                let selectedLayerNames = JSON.parse(layersInput.value);

                layerCheckboxes.each((index, element) => {
                    if(selectedLayerNames.includes(element.value)){
                        $(element).prop("checked", true);
                    }
                });
            }

           layerCheckboxes.on("click", {layerSelectorContainer, layersInput} ,this.onLayerClicked); 

        } catch (error) {
            console.error("Unable to get WMS capabilities! " + error);
            layersInput.value = "";
            
        } finally {
            this.toggleLoadButton(loadButton);
        }
    }   

    onLayerClicked(evt){
        let values = [];

        $(evt.data.layerSelectorContainer)
        .find("input[type='checkbox']:checked")
        .each((index, element) => values.push(element.value));
        
        evt.data.layersInput.value = JSON.stringify(values);
    }

    renderLayerSelector(layers, container) {
        let template = `<ul>`;
        template += this.getLayersTemplate(layers);
        template += `</ul>`;

        container.innerHTML = template;
    }

    getLayersTemplate(layers){
        let template = ``;
        
        layers.forEach(layer => {
            template += `
           <li>                    
                <div>
                    <input type="checkbox" value="${layer.name}">
                    <p>${layer.title}</p>         
                </div>
            `;

            if(layer.children && layer.children.length > 0){
                template += `
                <ul class="child-layers">
                   ${this.getLayersTemplate(layer.children)}                    
                </ul>     
                `;
            }

            template += `</li>`;
        });
        
        return template;
    }   

  async getCapabilities(url) {
    let urlObject = new URL(url); //throw away URL params, use following instead

        urlObject.searchParams.set("request", "GetCapabilities");
        urlObject.searchParams.set("service", "WMS");         

        return fetch(urlObject.toString().replace("=&", "&"))
            .then(response => response.text());
    }

    toggleLoadButton(buttonElement) {
        let iconElement = buttonElement.children[0];

        $(iconElement).toggle();
        buttonElement.disabled = !buttonElement.disabled;
    }

    getLayers(capabilitiesString) {
        let xmlDoc = new DOMParser().parseFromString(capabilitiesString, "text/xml");
        let result = xmlDoc.evaluate("/wms:WMS_Capabilities/wms:Capability/wms:Layer", xmlDoc, this.xPathNSResolver, XPathResult.FIRST_ORDERED_NODE_TYPE , null);
        let rootLayerNode = result.singleNodeValue;

        return this.parseChildLayers(xmlDoc, rootLayerNode);
    }

    parseChildLayers(xmlDoc, layerNode) {
        let childrenCountResult = xmlDoc.evaluate("count(wms:Layer)", layerNode, this.xPathNSResolver, XPathResult.NUMBER_TYPE, null);

        if(childrenCountResult.numberValue < 1){
            return [];
        }

        let childLayersIterator = xmlDoc.evaluate("wms:Layer", layerNode, this.xPathNSResolver, XPathResult.ORDERED_NODE_ITERATOR_TYPE, null);
        let thisChildLayer = childLayersIterator.iterateNext();
        let parsedLayers = [];

        while(thisChildLayer){
            parsedLayers.push({
                name: xmlDoc.evaluate("wms:Name[text()]", thisChildLayer, this.xPathNSResolver, XPathResult.STRING_TYPE, null).stringValue,                
                title: xmlDoc.evaluate("wms:Title[text()]", thisChildLayer, this.xPathNSResolver, XPathResult.STRING_TYPE, null).stringValue,
                abstract: xmlDoc.evaluate("wms:Abstract[text()]", thisChildLayer, this.xPathNSResolver, XPathResult.STRING_TYPE, null).stringValue,
                children: this.parseChildLayers(xmlDoc, thisChildLayer)
            })
            
            thisChildLayer = childLayersIterator.iterateNext();
        }

        return parsedLayers;
    }

    xPathNSResolver(prefix) {
        var namespaces = { wms: 'http://www.opengis.net/wms' };
        return namespaces[prefix];
    }
}

window.telepath.register('hslayers.blocks.WmsSourceBlock', WmsSourceBlockDefiniton);