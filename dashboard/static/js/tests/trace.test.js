function test_route_finder() {

    let dummyRouteWithMultipleRoutes = {
        found_at: "C",
        origin: "A",
        responses: {
            A: {
                timestamp_ms: 0,
                responded_with: ["B", "C", "D"],
            },
            B: {
                timestamp_ms: 12,
                responded_with: ["E", "C", "S"],
            },
            C: {
                timestamp_ms: 14,
                responded_with: ["L", "O"],
            },
        }
    };

    let successful_route = computeSuccessfulRoute(dummyRouteWithMultipleRoutes);
    console.assert(successful_route.length == 2);
    console.assert(successful_route.includes("A"));
    console.assert(successful_route.includes("C"));

}
