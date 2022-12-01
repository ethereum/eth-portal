
$(document).ready(function () {
    $('#start-query-button').click(function () {
        $('svg').remove();

        sendTraceContentRequest();
    });
});

// Sends a request for content with route info for where the content was found.
// Upon success, renders graph representation of the received data.
function sendTraceContentRequest() {

    var content_type = $("input[name='content-type']:checked").attr('id');
    var block_hash = $("#query-target").val();
    console.log(block_hash);

    $.get(`${content_type}/${block_hash}`, function (data) {
        if ('result' in data && 'trace' in data) {

            let graph_data = create_graph_data(data.trace);
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

// Converts json response to format expected by D3 ForceGraph:
// { nodes: [{ id, group }], links: [{ source_id, target_id, group }] }
// Group of nodes determines color, group of links determines thickness.
function create_graph_data(trace) {

    let successful_route = compute_successful_route(trace);

    // Create nodes.
    let nodes = [];
    let nodes_seen = [];
    let responses = trace.responses;
    Object.keys(responses).forEach((enr, _) => {

        let node = responses[enr];
        let responded_with = node.responded_with;
        if (!Array.isArray(responded_with)) {
            return;
        }
        if (!nodes_seen.includes(enr)) {
            let group = 0;
            if ('origin' in trace && trace['origin'] == enr) {
                group = 1;
            }
            if ('found_at' in trace && trace['found_at'] == enr) {
                group = 5;
            }
            nodes.push({ id: enr, group: group });
            nodes_seen.push(enr);
        }
    });

    // Create links.
    let links = [];
    Object.keys(responses).forEach((enr_source, _) => {

        let node = responses[enr_source];
        let responded_with = node.responded_with;
        if (!Array.isArray(responded_with)) {
            return;
        }
        responded_with.forEach((enr_target, _) => {
            if (!nodes_seen.includes(enr_target)) {
                let group = 0;
                if ('found_at' in trace && trace['found_at'] == enr_target) {
                    group = 5;
                }
                nodes.push({ id: enr_target, group: group })
                nodes_seen.push(enr_target)
            }
            let value = 1;
            if (successful_route.includes(enr_source)
                && successful_route.includes(enr_target)) {
                value = 20;
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

// Returns a list of nodes in the route, with `origin` as the first element and `found_at` as the last.
// Starts from the end (where the content was found) and finds the way back to the origin.
// Uses timestamps to decide between potential routes by seeing which response was available to be acted on sooner.
function compute_successful_route(trace) {

    if (!('origin' in trace
        && 'found_at' in trace)) {
        return [];
    }

    let origin = trace.origin;
    let found_at = trace.found_at;
    let responses = trace.responses;

    // Start at the end and work backwards.
    let target_node = found_at;
    let route = [];
    route.push(target_node);

    while (target_node != origin) {

        // Used to make sure the search has progressed.
        let previous_target = target_node;

        // Fastest response starts at infinity and comes down as smaller timestamps are found.
        let fastest_response_ms = Number.MAX_SAFE_INTEGER;

        // Find the node that first responded with `target_node`.
        for (node_id in responses) {

            let node = responses[node_id];
            // Validate node data.
            if (!('timestamp_ms' in node
                && 'responded_with' in node
                && Array.isArray(node.responded_with)
                && Number.isInteger(node.timestamp_ms))) {
                continue;
            }
            let timestamp = node.timestamp_ms;
            let responded_with = node.responded_with;

            if (responded_with.includes(target_node) && timestamp <= fastest_response_ms) {
                // Fastest response (so far) found.
                fastest_response_ms = timestamp;
                target_node = node_id;
            }

        }

        if (route.includes(target_node)) {
            // Loop detected, no route found.
            return [];
        } else if (previous_target == target_node) {
            // Search could not progress, no route found.
            return [];
        }
        else {
            route.push(target_node)
        }
    }

    // We currently have the final node first, and origin node last. Reverse for readability purposes.
    return route.reverse();

}

