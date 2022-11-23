
$(document).ready(function () {
    sendTraceContentRequest();
});

// Sends a request for content with route info for where the content was found.
// Upon success, renders graph representation of the received data.
function sendTraceContentRequest() {

    $.get(`trace/data`, function (data) {
        if ('result' in data && 'route' in data) {

            let graph_data = create_graph_data(data.route);
            render_graph(graph_data);

        } else {
            console.error('Received error from trace endpoint:');
            console.log(data);
        }
    },
        "json");

}

// Creates a D3 graph and adds it to the DOM.
function render_graph(graph_data) {

    let chart = ForceGraph(graph_data, {
        nodeId: d => d.id,
        nodeGroup: d => d.group,
        nodeTitle: d => `${d.id}\n${d.group}`,
        linkStrokeWidth: l => Math.sqrt(l.value),
        width: 1000,
        height: 600,
        invalidation: null
    });

    $('#d3-trace').before(chart);

}

// Converts json response to format expected by D3 ForceGraph.
function create_graph_data(route) {

    let nodes = [];
    route.forEach((enr, index) => {
        nodes.push({ id: enr, group: index });
    });
    let links = [];
    route.forEach((enr, index) => {
        if (index != (route.length - 1)) {
            links.push({
                source: enr,
                target: route[index + 1],
                value: 1
            })
        }
    });
    let graph = {
        nodes: nodes,
        links: links,
    }
    return graph;

}

