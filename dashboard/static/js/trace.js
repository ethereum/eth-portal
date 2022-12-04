$(document).ready(function () {

    $('#start-query-button').click(function () {
        $('svg').remove();
        sendTraceContentRequest();
    });
});

// Sends a request for content with route info for where the content was found.
// Upon success, renders graph representation of the received data.
function sendTraceContentRequest() {

    var block_hash = $("#query-target").val();
    if (block_hash.length === 0) { return };

    // Start loading animation.
    $('.spin').attr("hidden", false);

    var content_type = $("input[name='content-type']:checked").attr('id');
    $.get(`${content_type}/${block_hash}`, function (data) {
        if ('result' in data && 'trace' in data) {

            let result = data.result.content;
            renderResult(result)

            console.log('Graph:');
            console.log(data.trace);
            let graph_data = createGraphData(data.trace);
            renderGraph(graph_data);

        } else {
            console.error('Received error from trace endpoint:');
            console.log(data);
            renderResult(data.error);
        }
        $('.spin').attr("hidden", true);
    }, function (error) {
        console.error(error);
        $('.spin').attr("hidden", true);
    },
        "json");

}

function renderResult(result) {

    console.log('Result:');
    console.log(result);

    if (result === "0x") {
        result = "Not found.";
    }

    $('#results').attr("hidden", false);
    $('#result-value').text(result);

}

// Creates a D3 graph and adds it to the DOM.
function renderGraph(graph_data) {

    let chart = ForceGraph(graph_data, {
        nodeId: d => d.id,
        nodeGroup: d => d.group,
        nodeGroups: [0, 1, 2, 3, 4, 5, 6, 7, 9],
        nodeTitle: d => `${d.id}\n${d.timestamp === undefined ? '' : (d.timestamp + ' ms')}`,
        linkStrokeWidth: l => Math.sqrt(l.value),
        width: $('#graph').width(),
        height: $('#graph').height(),
        invalidation: null
    });

    $('#graph').append(chart);

}

// Converts json response to format expected by D3 ForceGraph:
// { nodes: [{ id, group }], links: [{ source_id, target_id, group }] }
// Group of nodes determines color, group of links determines thickness.
function createGraphData(trace) {

    // trace.found_content_at = "0x9ce72a5457eaa5264d929512ac8aeeedc6a2fe67b2591cde6eaab34f09d448e4";
    let successfulRoute = computeSuccessfulRoute(trace);

    const colors = {
        orange: 1,
        red: 2,
        blue: 0,
        green: 4,
        gray: 8,
    };

    console.log('Route:');
    console.log(successfulRoute);

    // Create nodes.
    let nodes = [];
    let nodesSeen = [];
    let responses = trace.responses;
    Object.keys(responses).forEach((enr, _) => {

        let node = responses[enr];
        let timestamp = node.timestamp_ms;
        let respondedWith = node.responded_with;
        if (!Array.isArray(respondedWith)) {
            return;
        }
        if (!nodesSeen.includes(enr)) {
            let group = 0;
            if ('origin' in trace && trace.origin == enr) {
                group = colors.orange;
            }
            else if ('found_content_at' in trace && trace.found_content_at == enr) {
                group = colors.green;
            } else {
                group = colors.blue;
            }
            nodes.push({ id: enr, group: group, timestamp: timestamp });
            nodesSeen.push(enr);
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
            if (!nodesSeen.includes(enr_target)) {
                let group = 0;
                if ('found_content_at' in trace && trace.found_content_at == enr_target) {
                    group = colors.green;
                } else {
                    group = colors.gray;
                }
                nodes.push({ id: enr_target, group: group })
                nodesSeen.push(enr_target)
            }
            let value = 1;
            if (successfulRoute.includes(enr_source)
                && successfulRoute.includes(enr_target)) {
                value = 40;
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

// Returns a list of nodes in the route.
// Starts from the end (where the content was found) and finds the way back to the origin.
function computeSuccessfulRoute(trace) {

    if (!('origin' in trace && 'found_content_at' in trace)) {
        return [];
    }

    let origin = trace.origin;
    let found_at = trace.found_content_at;

    let route = [];
    // Find the node that contains found_at.
    let target_node = found_at;
    route.push(target_node);
    let route_info = trace.responses;
    while (target_node != origin) {

        let previous_target = target_node;
        Object.keys(route_info).forEach((node_id, _) => {

            let node = route_info[node_id];
            let responses = node.responded_with;

            // Find the node that responded with the current target node.
            if (Array.isArray(responses) && responses.includes(target_node)) {
                target_node = node_id;
                route.push(target_node);
            }
        })
        if (previous_target == target_node) {
            // Did not progress, no route found.
            return [];
        }
    }
    return route;

}

