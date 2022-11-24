
$(document).ready(function () {
    sendTraceContentRequest();
});

// Sends a request for content with route info for where the content was found.
// Upon success, renders graph representation of the received data.
function sendTraceContentRequest() {

    $.get(`trace/header/0x56a9bb0302da44b8c0b3df540781424684c3af04d0b7a38d72842b762076a664`, function (data) {
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
    let routes = route.nodes_responded_with;
    Object.keys(routes).forEach((enr, index) => {
        let responded_with = routes[enr];
        if (!Array.isArray(responded_with)) {
            return;
        }
        if (!nodes_seen.includes(enr)) {
            let group = 0;
            if ('origin' in route && route['origin'] == enr) {
                group = 1;
            }
            nodes.push({ id: enr, group: group });
            nodes_seen.push(enr);
        }
    });
    let links = [];
    Object.keys(routes).forEach((enr_source, index) => {

        let responded_with = routes[enr_source];
        if (!Array.isArray(responded_with)) {
            return;
        }
        responded_with.forEach((enr_target, index) => {
            if (!nodes_seen.includes(enr_target)) {
                let group = 0;
                if ('found_content_at' in route && route['found_content_at'] == enr_target) {
                    group = 5;
                }
                nodes.push({ id: enr_target, group: group })
                nodes_seen.push(enr_target)
            }
            let value = 1;
            if (successful_route.includes(enr_source)
                && successful_route.includes(enr_target)) {
                value = 50;
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

    if (!('origin' in routes && 'found_content_at' in routes)) {
        return [];
    }

    let origin = routes['origin'];
    let found_at = routes['found_content_at'];

    let route = [];
    // Find the node that contains found_at
    let target_node = found_at;
    route.push(target_node);
    let route_info = routes.nodes_responded_with;
    while (target_node != origin) {
        Object.keys(route_info).forEach((node, index) => {
            if (Array.isArray(route_info[node]) && route_info[node].includes(target_node)) {
                target_node = node;
                route.push(target_node);
            }
        })
    }
    return route;

}

