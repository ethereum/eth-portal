
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
// Example input:
// {
//     "found_at": "S",
//     "origin": "A",
//     "A": ["B", "C", "D"],
//     "B": ["E", "F", "G"],
//     "C": ["E", "H", "I"],
//     "D": ["J", "K", "L", "E", "F"],
//     "E": ["X", "Y", "Z"],
//     "F": ["Q", "R", "S"],
//     "Q": ["X", "Y", "Z"],
// }
function create_graph_data(route) {

    console.log(route);
    let successful_route = compute_successful_route(route);

    let nodes = [];
    let nodes_seen = [];
    Object.keys(route).forEach((enr, index) => {
        let responded_with = route[enr];
        if (!Array.isArray(responded_with)) {
            return;
        }
        if (!nodes_seen.includes(enr)) {
            let group = 0;
            if ('origin' in route && route['origin'] == enr) {
                group = 1;
            }
            if ('found_at' in route && route['found_at'] == enr) {
                group = 2;
            }
            nodes.push({ id: enr, group: group });
            nodes_seen.push(enr);
        }
    });
    let links = [];
    Object.keys(route).forEach((enr_source, index) => {

        let responded_with = route[enr_source];
        if (!Array.isArray(responded_with)) {
            return;
        }
        responded_with.forEach((enr_target, index) => {
            if (!nodes_seen.includes(enr_target)) {
                nodes.push({ id: enr_target, group: 0 })
                nodes_seen.push(enr_target)
            }
            let value = 1;
            if (successful_route.includes(enr_source)
                && successful_route.includes(enr_target)) {
                value = 100;
            }
            links.push({
                source: enr_source,
                target: enr_target,
                value: value
            })
        })
    });
    let graph = {
        nodes: nodes,
        links: links,
    }
    return graph;

}

function compute_successful_route(routes) {

    if (!('origin' in routes && 'found_at' in routes)) {
        return [];
    }

    let origin = routes['origin'];
    let found_at = routes['found_at'];

    let route = [];
    // Find the node that contains found_at
    let target_node = found_at;
    route.push(target_node);
    while (target_node != origin) {
        Object.keys(routes).forEach((node, index) => {
            if (Array.isArray(routes[node]) && routes[node].includes(target_node)) {
                target_node = node;
                route.push(target_node);
            }
        })
    }
    return route;

}

