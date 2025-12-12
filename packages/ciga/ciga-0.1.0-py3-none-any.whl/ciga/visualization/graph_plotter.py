import os
import json
import threading
import webbrowser
import urllib.parse
from http.server import SimpleHTTPRequestHandler, HTTPServer
from functools import partial
import numpy as np


def _graph_to_vis_json(graph):
    """Convert igraph Graph to vis.js JSON format with bidirectional edge handling"""
    if graph is None or graph.vcount() == 0:
        return {"nodes": [], "edges": []}
    
    # Calculate layout
    layout = graph.layout("fr")
    layout.fit_into(bbox=(-600, -600, 600, 600))
    
    # Build nodes
    nodes = []
    for v in graph.vs:
        name = v["name"] if "name" in v.attributes() else str(v.index)
        x, y = layout.coords[v.index]
        nodes.append({"id": v.index, "label": name, "x": x, "y": -y})
    
    # Build edges with bidirectional handling
    edge_map = {}
    for e in graph.es:
        edge_map[(e.source, e.target)] = e
    
    edges = []
    processed = set()
    for e in graph.es:
        src, tgt = e.source, e.target
        if (src, tgt) in processed:
            continue
        weight = e["weight"] if "weight" in e.attributes() else 1
        
        if graph.is_directed() and (tgt, src) in edge_map:
            # Bidirectional
            processed.add((src, tgt))
            processed.add((tgt, src))
            rev = edge_map[(tgt, src)]
            rev_w = rev["weight"] if "weight" in rev.attributes() else 1
            edges.append({
                "from": src, "to": tgt,
                "label": f"◀ {rev_w:.1f}    {weight:.1f} ▶",
                "arrows": "to;from"
            })
        else:
            processed.add((src, tgt))
            edges.append({
                "from": src, "to": tgt,
                "label": f"{weight:.1f}",
                "arrows": "to" if graph.is_directed() else ""
            })
    
    return {"nodes": nodes, "edges": edges}


def _generate_graph_html(graph_json):
    """Generate standalone HTML for graph visualization"""
    return '''<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Graph Viewer</title>
    <script src="https://cdnjs.cloudflare.com/ajax/libs/vis-network/9.1.2/dist/vis-network.min.js"></script>
    <style>
        *{margin:0;padding:0;box-sizing:border-box}
        body{font:13px/1.4 -apple-system,system-ui,sans-serif;display:flex;height:100vh;color:#333;overflow:hidden}
        .side{width:240px;padding:16px;background:#f8f8f8;overflow-y:auto;flex-shrink:0;border-right:1px solid #ddd}
        .main{flex:1;display:flex;flex-direction:column;height:100vh;overflow:hidden}
        .bar{display:flex;justify-content:space-between;padding:8px 16px;background:#f8f8f8;font-size:12px;color:#888;border-bottom:1px solid #ddd;flex-shrink:0}
        .bar button{padding:3px 8px;border:1px solid #ccc;background:#fff;cursor:pointer;font-size:11px}
        .bar button:hover{background:#eee}
        #graph{flex:1;background:#fff;position:relative;overflow:hidden;visibility:hidden}
        #graph.show{visibility:visible}
        h1{font-size:14px;font-weight:500;margin-bottom:14px;color:#222}
        .sec{margin-bottom:12px}
        .sec-title{font-size:10px;color:#999;text-transform:uppercase;letter-spacing:.5px;margin-bottom:6px;cursor:pointer;display:flex;justify-content:space-between}
        .sec-title.fold .arr{transform:rotate(-90deg)}
        .sec-body{transition:all .15s}
        .sec-body.fold{height:0;overflow:hidden;opacity:0}
        .row{display:flex;align-items:center;gap:8px;margin-bottom:8px}
        .row label{width:55px;font-size:11px;color:#666}
        .row input[type=range]{flex:1;height:1px;-webkit-appearance:none;background:#ddd}
        .row input[type=range]::-webkit-slider-thumb{-webkit-appearance:none;width:8px;height:8px;background:#333;border-radius:50%;cursor:pointer}
        .row input[type=color]{width:24px;height:18px;border:1px solid #ddd;padding:0;cursor:pointer}
        .row .v{width:24px;text-align:right;font-size:11px;color:#888}
    </style>
</head>
<body>
    <div class="side">
        <h1>Graph Viewer</h1>
        <div class="sec">
            <div class="sec-title" onclick="this.classList.toggle('fold');this.nextElementSibling.classList.toggle('fold')">Style <span class="arr">▼</span></div>
            <div class="sec-body">
                <div class="row"><label>Node</label><input type="range" id="node-size" min="2" max="100" value="12" oninput="us()"><span class="v" id="v-ns">12</span></div>
                <div class="row"><label>Fill</label><input type="color" id="node-color" value="#ffffff" oninput="us()"></div>
                <div class="row"><label>Stroke</label><input type="range" id="border-width" min="0.5" max="10" step="0.5" value="1.5" oninput="us()"><span class="v" id="v-bw">1.5</span></div>
                <div class="row"><label>Color</label><input type="color" id="border-color" value="#000000" oninput="us()"></div>
                <div class="row"><label>Edge</label><input type="range" id="edge-width" min="0.5" max="20" step="0.5" value="1.5" oninput="us()"><span class="v" id="v-ew">1.5</span></div>
                <div class="row"><label>Color</label><input type="color" id="edge-color" value="#000000" oninput="us()"></div>
                <div class="row"><label>Font</label><input type="range" id="font-size" min="4" max="72" value="12" oninput="us()"><span class="v" id="v-fs">12</span></div>
                <div class="row"><label>Color</label><input type="color" id="font-color" value="#000000" oninput="us()"></div>
                <div class="row"><label>Distance</label><input type="range" id="distance" min="0.1" max="5" step="0.1" value="1" oninput="applyDistance()"><span class="v" id="v-dist">1.0</span></div>
            </div>
        </div>
    </div>
    <div class="main">
        <div class="bar"><span>Nodes: <b id="nc">0</b> | Edges: <b id="ec">0</b></span><button onclick="fitView()">Fit View</button><button onclick="exportSVG()">Export SVG</button></div>
        <div id="graph"></div>
    </div>
    <script>
        const DATA = ''' + json.dumps(graph_json) + ''';
        let network=null,distance=1,basePos={};
        let S={nodeSize:12,nodeColor:'#fff',borderColor:'#000',borderWidth:1.5,edgeWidth:1.5,edgeColor:'#000',fontSize:12,fontColor:'#000'};
        const $=id=>document.getElementById(id);
        function us(){
            S.nodeSize=+$('node-size').value;S.nodeColor=$('node-color').value;S.borderColor=$('border-color').value;
            S.borderWidth=+$('border-width').value;S.edgeWidth=+$('edge-width').value;S.edgeColor=$('edge-color').value;
            S.fontSize=+$('font-size').value;S.fontColor=$('font-color').value;
            $('v-ns').innerText=S.nodeSize;$('v-bw').innerText=S.borderWidth;$('v-ew').innerText=S.edgeWidth;$('v-fs').innerText=S.fontSize;
            render(true);
        }
        function applyDistance(){distance=+$('distance').value;$('v-dist').innerText=distance.toFixed(1);if(network&&basePos){network.body.data.nodes.update(Object.keys(basePos).map(id=>({id:+id,x:basePos[id].x*distance,y:basePos[id].y*distance})));}}
        function fitView(){if(network)network.fit();}
        function render(keepView=false){
            const container=$('graph');
            container.classList.remove('show');
            const savedView=(network&&keepView)?{scale:network.getScale(),position:network.getViewPosition()}:null;
            basePos={};DATA.nodes.forEach(n=>{basePos[n.id]={x:n.x,y:n.y};});
            const nodes=new vis.DataSet(DATA.nodes.map(n=>({id:n.id,label:n.label,x:n.x*distance,y:n.y*distance,
                color:{background:S.nodeColor,border:S.borderColor,highlight:{background:'#eee',border:S.borderColor}},
                font:{color:S.fontColor,size:S.fontSize}})));
            const edges=new vis.DataSet(DATA.edges.map(e=>({from:e.from,to:e.to,label:e.label,arrows:e.arrows,smooth:false,
                color:{color:S.edgeColor},font:{color:S.fontColor,size:S.fontSize*0.8,strokeWidth:2,strokeColor:'#fff',align:'top'}})));
            if(network)network.destroy();
            network=new vis.Network(container,{nodes,edges},{autoResize:true,width:'100%',height:'100%',
                nodes:{shape:'dot',size:S.nodeSize,borderWidth:S.borderWidth},edges:{width:S.edgeWidth},
                physics:{enabled:false},layout:{improvedLayout:false},interaction:{dragNodes:true,dragView:true,zoomView:true}});
            $('nc').textContent=DATA.nodes.length;$('ec').textContent=DATA.edges.length;
            network.once('afterDrawing',()=>{if(savedView){network.moveTo({position:savedView.position,scale:savedView.scale,animation:false});}else{network.fit();}requestAnimationFrame(()=>container.classList.add('show'));});
        }
        function exportSVG(){
            if(!network)return;
            const pos=network.getPositions(),ids=Object.keys(pos);if(!ids.length)return;
            let minX=Infinity,minY=Infinity,maxX=-Infinity,maxY=-Infinity;
            ids.forEach(id=>{const p=pos[id];minX=Math.min(minX,p.x);minY=Math.min(minY,p.y);maxX=Math.max(maxX,p.x);maxY=Math.max(maxY,p.y);});
            const pad=80,w=maxX-minX+pad*2,h=maxY-minY+pad*2,ox=-minX+pad,oy=-minY+pad;
            let svg=`<svg xmlns="http://www.w3.org/2000/svg" width="${w}" height="${h}" viewBox="0 0 ${w} ${h}"><style>text{font-family:sans-serif}</style><rect width="100%" height="100%" fill="#fff"/>`;
            network.body.data.edges.get().forEach(e=>{const p1=pos[e.from],p2=pos[e.to];if(!p1||!p2)return;
                const x1=p1.x+ox,y1=p1.y+oy,x2=p2.x+ox,y2=p2.y+oy;
                svg+=`<line x1="${x1}" y1="${y1}" x2="${x2}" y2="${y2}" stroke="${S.edgeColor}" stroke-width="${S.edgeWidth}"/>`;
                if(e.label){const ly=(y1+y2)/2-8;svg+=`<text x="${(x1+x2)/2}" y="${ly}" text-anchor="middle" fill="${S.fontColor}" font-size="${S.fontSize}" stroke="#fff" stroke-width="2" paint-order="stroke">${e.label}</text>`;}
                const a=Math.atan2(y2-y1,x2-x1),r=S.nodeSize+S.edgeWidth,ax=x2-r*Math.cos(a),ay=y2-r*Math.sin(a),hl=6*S.edgeWidth/1.5;
                svg+=`<polygon points="${ax},${ay} ${ax-hl*Math.cos(a-Math.PI/6)},${ay-hl*Math.sin(a-Math.PI/6)} ${ax-hl*Math.cos(a+Math.PI/6)},${ay-hl*Math.sin(a+Math.PI/6)}" fill="${S.edgeColor}"/>`;
            });
            network.body.data.nodes.get().forEach(n=>{const p=pos[n.id];if(!p)return;const x=p.x+ox,y=p.y+oy;
                svg+=`<circle cx="${x}" cy="${y}" r="${S.nodeSize}" fill="${S.nodeColor}" stroke="${S.borderColor}" stroke-width="${S.borderWidth}"/>`;
                if(n.label)svg+=`<text x="${x}" y="${y+S.nodeSize+S.fontSize+2}" text-anchor="middle" fill="${S.fontColor}" font-size="${S.fontSize}">${n.label}</text>`;
            });
            svg+='</svg>';
            const link=document.createElement('a');link.download='graph.svg';link.href='data:image/svg+xml;charset=utf-8,'+encodeURIComponent(svg);link.click();
        }
        render();
    </script>
</body>
</html>'''


def graph_viz(graph, output_file='graph.html', port=None, open_browser=True):
    """
    Create an interactive graph visualization with the same style as tgraph_viz.
    
    Features:
    - Clean black-and-white style
    - Proper bidirectional edge labels (no overlap)
    - Style controls (node size, colors, edge width, font, scale)
    - SVG export
    - Draggable nodes
    
    Args:
        graph: igraph Graph object
        output_file: output HTML file path (used if port is None)
        port: if specified, starts a local server on this port
        open_browser: whether to open browser automatically
    
    Returns:
        If port is None: saves HTML file and returns file path
        If port is specified: returns HTTPServer instance
    
    Example:
        >>> import ciga as cg
        >>> g = cg.TGraph(...).get_graph(accumulate=True)
        >>> cg.graph_viz(g, 'my_graph.html')  # Save to file
        >>> cg.graph_viz(g, port=8080)  # Start server
    """
    graph_json = _graph_to_vis_json(graph)
    html = _generate_graph_html(graph_json)
    
    if port is None:
        # Save to file
        with open(output_file, 'w', encoding='utf-8') as f:
            f.write(html)
        if open_browser:
            webbrowser.open(f'file://{os.path.abspath(output_file)}')
        return output_file
    else:
        # Start server
        class Handler(SimpleHTTPRequestHandler):
            def do_GET(self):
                self.send_response(200)
                self.send_header('Content-type', 'text/html')
                self.end_headers()
                self.wfile.write(html.encode('utf-8'))
            def log_message(self, *args): pass
        
        server = HTTPServer(('localhost', port), Handler)
        if open_browser:
            webbrowser.open(f'http://localhost:{port}')
        print(f"Graph visualization at http://localhost:{port}")
        threading.Thread(target=server.serve_forever, daemon=True).start()
        return server


def _calculate_global_layout(tgraph):
    """Calculate a global layout based on the full accumulated graph"""
    # Get the full graph (accumulated up to the end)
    # We use a large time point to ensure we get everything
    full_graph = tgraph.get_graph(accumulate=True)
    
    if full_graph is None or full_graph.vcount() == 0:
        return {}
        
    # Use igraph's layout method (Fruchterman-Reingold)
    # This creates a visually pleasing layout
    layout = full_graph.layout("fr")
    
    # Normalize layout to fit in a reasonable box for vis.js
    # vis.js default canvas is roughly -1000 to 1000
    layout.fit_into(bbox=(-800, -800, 800, 800))
    
    pos_map = {}
    for v, (x, y) in zip(full_graph.vs, layout.coords):
        # Key by name if available, else index
        key = v["name"] if "name" in v.attributes() else str(v.index)
        # Flip Y coordinate because vis.js/canvas Y is down, but mathematical Y is up
        # Though often not strictly necessary, it matches expectation
        pos_map[key] = {"x": x, "y": -y}
        
    return pos_map


def _graph_to_json(graph, pos_map=None):
    """Convert an igraph Graph to JSON format for vis.js"""
    if graph is None or graph.vcount() == 0:
        return {"nodes": [], "edges": []}
    
    nodes = []
    for v in graph.vs:
        name = v["name"] if "name" in v.attributes() else str(v.index)
        node_data = {"id": v.index, "label": name}
        
        # Apply fixed position if available
        if pos_map and name in pos_map:
            node_data["x"] = pos_map[name]["x"]
            node_data["y"] = pos_map[name]["y"]
            # Fix the node so physics doesn't move it
            # But allow user to drag it (physics: false disables simulation for this node)
            node_data["physics"] = False
            
        nodes.append(node_data)
    
    # Build edge map
    edge_map = {}
    for e in graph.es:
        edge_map[(e.source, e.target)] = e
    
    edges = []
    processed_pairs = set()
    
    for e in graph.es:
        src, tgt = e.source, e.target
        if (src, tgt) in processed_pairs:
            continue
            
        weight = e["weight"] if "weight" in e.attributes() else 1
        
        if (tgt, src) in edge_map:
            # Bidirectional
            processed_pairs.add((src, tgt))
            processed_pairs.add((tgt, src))
            
            rev_edge = edge_map[(tgt, src)]
            rev_weight = rev_edge["weight"] if "weight" in rev_edge.attributes() else 1
            
            # Combined edge with custom label
            # Format:  <- (rev_weight)  (weight) ->
            edges.append({
                "from": src,
                "to": tgt,
                "value": max(weight, rev_weight), # Use max for scaling if needed
                "label": f"◀ {rev_weight:.1f}    {weight:.1f} ▶",
                "arrows": "to;from",
                "color": "#000",
                "font": {"align": "top", "color": "#000", "strokeWidth": 2, "strokeColor": "#fff"}
            })
        else:
            # Unidirectional
            processed_pairs.add((src, tgt))
            edges.append({
                "from": src,
                "to": tgt,
                "value": weight,
                "label": f"{weight:.1f}",
                "arrows": "to",
                "color": "#000",
                "font": {"align": "top", "color": "#000", "strokeWidth": 2, "strokeColor": "#fff"}
            })
    
    return {"nodes": nodes, "edges": edges}


class TGraphCache:
    """
    LRU cache for TGraph visualizations.
    Stores pre-computed graphs and their JSON representations for faster access.
    """
    def __init__(self, tgraph, max_size=50):
        self.tgraph = tgraph
        self.max_size = max_size
        self._cache = {}  # key: (mode, time_tuple) -> graph_json
        self._access_order = []  # for LRU eviction
        
        # Pre-calculate global layout
        # print("[Cache] Calculating global layout...", flush=True)
        self._global_layout = _calculate_global_layout(tgraph)
        # print(f"[Cache] Global layout calculated for {len(self._global_layout)} nodes", flush=True)
    
    def _make_key(self, mode, start, end):
        """Create a hashable cache key"""
        return (mode, tuple(start) if start else None, tuple(end) if end else None)
    
    def get_graph_json(self, mode, start, end):
        """
        Get graph JSON, using cache if available.
        Uses lazy loading - only computes when needed.
        
        If start is None, it means "from the very beginning" (∅).
        """
        key = self._make_key(mode, start, end)
        
        # Check cache first
        if key in self._cache:
            # Move to end of access order (most recently used)
            self._access_order.remove(key)
            self._access_order.append(key)
            # print(f"[Cache] HIT: {key}", flush=True)
            return self._cache[key]
        
        # print(f"[Cache] MISS: {key}, computing...", flush=True)
        
        # Compute the graph
        try:
            if mode == 'cumulative':
                time_point = tuple(end) if end else None
                graph = self.tgraph.get_graph(time_point=time_point, accumulate=True)
            else:  # delta mode
                start_point = tuple(start) if start else None
                end_point = tuple(end) if end else None
                graph = self.tgraph.get_delta_graph(start=start_point, end=end_point)
            
            # Pass the global layout to JSON converter
            graph_json = _graph_to_json(graph, pos_map=self._global_layout)
        except Exception as e:
            import traceback
            # print(f"[Cache] Error computing graph: {e}", flush=True)
            traceback.print_exc()
            return {"nodes": [], "edges": [], "error": str(e)}
        
        # Add to cache
        self._cache[key] = graph_json
        self._access_order.append(key)
        
        # Evict oldest if cache is full
        while len(self._cache) > self.max_size:
            oldest_key = self._access_order.pop(0)
            del self._cache[oldest_key]
            # print(f"[Cache] Evicted: {oldest_key}", flush=True)
        
        # print(f"[Cache] Stored: {key}, cache size: {len(self._cache)}", flush=True)
        return graph_json
    
    def clear(self):
        """Clear the cache"""
        self._cache.clear()
        self._access_order.clear()


def _get_time_index_structure(tgraph):
    """Extract hierarchical time index structure from TGraph for cascading sliders"""
    data = tgraph.data.reset_index()
    position_cols = list(tgraph._position)
    
    # Build hierarchical structure
    # For each combination of parent values, store available child values
    structure = {
        "levels": position_cols,
        "hierarchy": {}
    }
    
    # Build the hierarchy tree
    for i, col in enumerate(position_cols):
        if i == 0:
            # Top level - just unique values
            structure["hierarchy"][col] = {
                "values": sorted(data[col].unique().tolist()),
                "parent": None
            }
        else:
            # Child levels - group by parent columns
            parent_cols = position_cols[:i]
            grouped = data.groupby(parent_cols)[col].apply(lambda x: sorted(x.unique().tolist()))
            
            # Convert to dict with tuple keys as strings
            hierarchy_dict = {}
            for key, values in grouped.items():
                # Convert tuple key to string for JSON
                key_str = str(key) if isinstance(key, tuple) else str((key,))
                hierarchy_dict[key_str] = values
            
            structure["hierarchy"][col] = {
                "values": sorted(data[col].unique().tolist()),  # all possible values
                "parent": position_cols[i-1],
                "by_parent": hierarchy_dict
            }
    
    return structure


def _generate_html_template():
    """Generate a minimal HTML template for TGraph visualization"""
    return '''<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>TGraph</title>
    <script src="https://cdnjs.cloudflare.com/ajax/libs/vis-network/9.1.2/dist/vis-network.min.js"></script>
    <style>
        *{margin:0;padding:0;box-sizing:border-box}
        body{font:13px/1.4 -apple-system,system-ui,sans-serif;display:flex;height:100vh;color:#333;overflow:hidden}
        .side{width:280px;padding:16px;background:#f8f8f8;overflow-y:auto;flex-shrink:0;border-right:1px solid #ddd}
        .main{flex:1;display:flex;flex-direction:column;height:100vh;overflow:hidden}
        .bar{display:flex;justify-content:space-between;padding:8px 16px;background:#f8f8f8;font-size:12px;color:#888;border-bottom:1px solid #ddd;flex-shrink:0}
        .bar button{padding:3px 8px;border:1px solid #ccc;background:#fff;cursor:pointer;font-size:11px}
        .bar button:hover{background:#eee}
        #graph{flex:1;background:#fff;position:relative;overflow:hidden;visibility:hidden}
        #graph.show{visibility:visible}
        h1{font-size:14px;font-weight:500;margin-bottom:14px;color:#222}
        .tabs{display:flex;gap:6px;margin-bottom:14px}
        .tabs button{flex:1;padding:5px;border:1px solid #ddd;background:#fff;cursor:pointer;font-size:12px;transition:all .15s}
        .tabs button.on{background:#333;color:#fff;border-color:#333}
        .sec{margin-bottom:12px}
        .sec-title{font-size:10px;color:#999;text-transform:uppercase;letter-spacing:.5px;margin-bottom:6px;cursor:pointer;display:flex;justify-content:space-between}
        .sec-title.fold .arr{transform:rotate(-90deg)}
        .sec-body{transition:all .15s}
        .sec-body.fold{height:0;overflow:hidden;opacity:0}
        .row{display:flex;align-items:center;gap:8px;margin-bottom:8px}
        .row label{width:55px;font-size:11px;color:#666}
        .row input[type=range]{flex:1;height:1px;-webkit-appearance:none;background:#ddd}
        .row input[type=range]::-webkit-slider-thumb{-webkit-appearance:none;width:8px;height:8px;background:#333;border-radius:50%;cursor:pointer}
        .row input[type=color]{width:24px;height:18px;border:1px solid #ddd;padding:0;cursor:pointer}
        .row .v{width:24px;text-align:right;font-size:11px;color:#888}
        .chk{display:flex;align-items:center;gap:5px;margin-bottom:8px;font-size:12px}
        .btn{width:100%;padding:7px;background:#333;border:none;color:#fff;font-size:11px;cursor:pointer;margin-top:6px}
        .btn:hover{background:#555}
        .hide{display:none}
        .off{opacity:.3;pointer-events:none}
    </style>
</head>
<body>
    <div class="side">
        <h1>TGraph Viewer</h1>
        <div class="tabs">
            <button class="on" data-mode="cumulative">Cumulative</button>
            <button data-mode="delta">Delta</button>
        </div>
        <div id="start-sec" class="sec hide">
            <div class="sec-title">Start Point</div>
            <div class="chk"><input type="checkbox" id="from-start" checked><label for="from-start">From beginning</label></div>
            <div id="start-sliders"></div>
        </div>
        <div class="sec">
            <div class="sec-title">End Point</div>
            <div id="end-sliders"></div>
            <button class="btn" onclick="updateGraph()">Update</button>
        </div>
        <div class="sec">
            <div class="sec-title fold" onclick="this.classList.toggle('fold');this.nextElementSibling.classList.toggle('fold')">Style <span class="arr">▼</span></div>
            <div class="sec-body fold">
                <div class="row"><label>Node</label><input type="range" id="node-size" min="2" max="100" value="12" oninput="us()"><span class="v" id="v-ns">12</span></div>
                <div class="row"><label>Fill</label><input type="color" id="node-color" value="#ffffff" oninput="us()"></div>
                <div class="row"><label>Stroke</label><input type="range" id="border-width" min="0.5" max="10" step="0.5" value="1.5" oninput="us()"><span class="v" id="v-bw">1.5</span></div>
                <div class="row"><label>Color</label><input type="color" id="border-color" value="#000000" oninput="us()"></div>
                <div class="row"><label>Edge</label><input type="range" id="edge-width" min="0.5" max="20" step="0.5" value="1.5" oninput="us()"><span class="v" id="v-ew">1.5</span></div>
                <div class="row"><label>Color</label><input type="color" id="edge-color" value="#000000" oninput="us()"></div>
                <div class="row"><label>Font</label><input type="range" id="font-size" min="4" max="72" value="12" oninput="us()"><span class="v" id="v-fs">12</span></div>
                <div class="row"><label>Color</label><input type="color" id="font-color" value="#000000" oninput="us()"></div>
                <div class="row"><label>Distance</label><input type="range" id="distance" min="0.1" max="5" step="0.1" value="1" oninput="applyDistance()"><span class="v" id="v-dist">1.0</span></div>
            </div>
        </div>
    </div>
    <div class="main">
        <div class="bar"><span>Nodes: <b id="node-count">0</b> | Edges: <b id="edge-count">0</b></span><button onclick="fitView()">Fit View</button><button onclick="exportSVG()">Export SVG</button></div>
        <div id="graph"></div>
    </div>
    <script>
        let structure=null,network=null,mode='cumulative',currentData=null,distance=1,basePositions=null,customPositions={};
        let S={nodeSize:12,nodeColor:'#fff',borderColor:'#000',borderWidth:1.5,edgeWidth:1.5,edgeColor:'#000',fontSize:12,fontColor:'#000'};
        const $=id=>document.getElementById(id);
        function us(){
            S.nodeSize=+$('node-size').value;S.nodeColor=$('node-color').value;S.borderColor=$('border-color').value;
            S.borderWidth=+$('border-width').value;S.edgeWidth=+$('edge-width').value;S.edgeColor=$('edge-color').value;
            S.fontSize=+$('font-size').value;S.fontColor=$('font-color').value;
            $('v-ns').innerText=S.nodeSize;$('v-bw').innerText=S.borderWidth;$('v-ew').innerText=S.edgeWidth;$('v-fs').innerText=S.fontSize;
            if(currentData)renderGraph(currentData,true);
        }
        function applyDistance(){distance=+$('distance').value;$('v-dist').innerText=distance.toFixed(1);if(network&&basePositions){network.body.data.nodes.update(Object.keys(basePositions).map(id=>({id:+id,x:basePositions[id].x*distance,y:basePositions[id].y*distance})));}}
        function fitView(){if(network)network.fit();}
        function exportSVG() {
            if (!network) { alert('No graph'); return; }
            try {
                const pos = network.getPositions(), ids = Object.keys(pos);
                if (!ids.length) { alert('No nodes'); return; }
                let minX=Infinity,minY=Infinity,maxX=-Infinity,maxY=-Infinity;
                ids.forEach(id => { const p=pos[id]; minX=Math.min(minX,p.x);minY=Math.min(minY,p.y);maxX=Math.max(maxX,p.x);maxY=Math.max(maxY,p.y); });
                const pad=80, w=maxX-minX+pad*2, h=maxY-minY+pad*2, ox=-minX+pad, oy=-minY+pad;
                let svg=`<svg xmlns="http://www.w3.org/2000/svg" width="${w}" height="${h}" viewBox="0 0 ${w} ${h}"><style>text{font-family:sans-serif}</style><rect width="100%" height="100%" fill="#fff"/>`;
                network.body.data.edges.get().forEach(e => {
                    const p1=pos[e.from],p2=pos[e.to]; if(!p1||!p2)return;
                    const x1=p1.x+ox,y1=p1.y+oy,x2=p2.x+ox,y2=p2.y+oy,c=e.color?.color==='#888'?'#888':S.edgeColor;
                    svg+=`<line x1="${x1}" y1="${y1}" x2="${x2}" y2="${y2}" stroke="${c}" stroke-width="${S.edgeWidth}"/>`;
                    if(e.label){const ly=(y1+y2)/2+(e.font?.align==='top'?-8:e.font?.align==='bottom'?12:0);svg+=`<text x="${(x1+x2)/2}" y="${ly}" text-anchor="middle" fill="${e.font?.color||S.fontColor}" font-size="${S.fontSize}" stroke="#fff" stroke-width="2" paint-order="stroke">${e.label}</text>`;}
                    const a=Math.atan2(y2-y1,x2-x1),r=S.nodeSize+S.edgeWidth,ax=x2-r*Math.cos(a),ay=y2-r*Math.sin(a),hl=6*S.edgeWidth/1.5;
                    svg+=`<polygon points="${ax},${ay} ${ax-hl*Math.cos(a-Math.PI/6)},${ay-hl*Math.sin(a-Math.PI/6)} ${ax-hl*Math.cos(a+Math.PI/6)},${ay-hl*Math.sin(a+Math.PI/6)}" fill="${c}"/>`;
                });
                network.body.data.nodes.get().forEach(n => {
                    const p=pos[n.id];if(!p)return;const x=p.x+ox,y=p.y+oy;
                    svg+=`<circle cx="${x}" cy="${y}" r="${S.nodeSize}" fill="${S.nodeColor}" stroke="${S.borderColor}" stroke-width="${S.borderWidth}"/>`;
                    if(n.label)svg+=`<text x="${x}" y="${y+S.nodeSize+S.fontSize+2}" text-anchor="middle" fill="${S.fontColor}" font-size="${S.fontSize}">${n.label}</text>`;
                });
                svg+='</svg>';
                const link=document.createElement('a');link.download='tgraph.svg';
                link.href = 'data:image/svg+xml;charset=utf-8,' + encodeURIComponent(svg); link.click();
            } catch(err) { alert('SVG export error: ' + err.message); console.error(err); }
        }
        
        async function init() {
            structure = await (await fetch('/api/time_structure')).json();
            buildSliders(); setupFromBeginning(); updateGraph();
        }
        
        function buildSliders() {
            const L=structure.levels,H=structure.hierarchy;
            ['start','end'].forEach(p=>{const c=$(p+'-sliders');c.innerHTML='';L.forEach((l,i)=>{const v=H[l].values,mn=Math.min(...v),mx=Math.max(...v),d=p==='start'?mn:mx;c.innerHTML+=`<div class="row"><label>${l}</label><input type="range" id="${p}-${l}" min="${mn}" max="${mx}" value="${d}" data-level="${l}" data-index="${i}"><span class="v" id="${p}-${l}-val">${d}</span></div>`;});});
            document.querySelectorAll('input[type="range"]').forEach(s=>s.addEventListener('input',e=>onSliderChange(e.target)));
            // Cascade update child sliders based on initial parent values
            ['start','end'].forEach(p=>updateChildSliders(p,0));
        }
        function setupFromBeginning(){const cb=$('from-start'),ss=$('start-sliders');cb.addEventListener('change',()=>ss.classList.toggle('off',cb.checked));ss.classList.add('off');}
        function onSliderChange(s){const[p]=s.id.split('-');$(`${p}-${s.dataset.level}-val`).textContent=s.value;updateChildSliders(p,+s.dataset.index);}
        function updateChildSliders(p,pi){const L=structure.levels,H=structure.hierarchy;for(let i=pi+1;i<L.length;i++){const l=L[i],info=H[l];if(!info.by_parent)continue;const pv=L.slice(0,i).map(x=>+$(`${p}-${x}`).value),av=info.by_parent['('+pv.join(', ')+')']||info.values,s=$(`${p}-${l}`),mn=Math.min(...av),mx=Math.max(...av);s.min=mn;s.max=mx;let v=+s.value;if(v<mn)v=mn;if(v>mx)v=mx;s.value=v;$(`${p}-${l}-val`).textContent=v;}}
        document.querySelectorAll('.tabs button').forEach(b=>{b.addEventListener('click',()=>{document.querySelectorAll('.tabs button').forEach(x=>x.classList.remove('on'));b.classList.add('on');mode=b.dataset.mode;$('start-sec').classList.toggle('hide',mode==='cumulative');});});
        async function updateGraph(){const L=structure.levels,fs=$('from-start').checked;let sp=fs?null:L.map(l=>+$(`start-${l}`).value);const ep=L.map(l=>+$(`end-${l}`).value),r=await fetch(`/api/graph?${new URLSearchParams({mode,start:JSON.stringify(sp),end:JSON.stringify(ep)})}`),d=await r.json();const isFirst=!currentData;currentData=d;$('node-count').textContent=d.nodes.length;$('edge-count').textContent=d.edges.length;renderGraph(d,!isFirst);if(isFirst&&network)network.fit();}
        
        function renderGraph(data, keepView=false) {
            const container = $('graph');
            // Hide graph during transition to prevent flicker
            container.classList.remove('show');
            // Save current view state before destroying network
            const savedView = (network && keepView) ? {scale: network.getScale(), position: network.getViewPosition()} : null;
            basePositions = {};
            data.nodes.forEach(n => { 
                if(customPositions[n.id]){n.x=customPositions[n.id].x;n.y=customPositions[n.id].y;}
                basePositions[n.id] = {x: n.x, y: n.y}; 
            });
            const nodes = new vis.DataSet(data.nodes.map(n => ({
                id: n.id, label: n.label, x: n.x * distance, y: n.y * distance,
                color: {background: S.nodeColor, border: S.borderColor, highlight: {background: '#eee', border: S.borderColor}},
                font: {color: S.fontColor, size: S.fontSize}
            })));
            const edges = new vis.DataSet(data.edges.map(e => ({
                from: e.from, to: e.to, label: e.label, arrows: e.arrows, smooth: false,
                color: {color: e.secondary ? '#888' : S.edgeColor},
                font: {color: e.secondary ? '#888' : S.fontColor, size: S.fontSize * 0.8, strokeWidth: 2, strokeColor: '#fff', align: e.font?.align || 'horizontal'}
            })));
            const options = {
                autoResize: true, width: '100%', height: '100%',
                nodes: {shape: 'dot', size: S.nodeSize, borderWidth: S.borderWidth},
                edges: {width: S.edgeWidth},
                physics: {enabled: false}, layout: {improvedLayout: false},
                interaction: {dragNodes: true, dragView: true, zoomView: true}
            };
            if (network) network.destroy();
            network = new vis.Network(container, {nodes, edges}, options);
            // Wait for first render, then restore view and show
            network.once('afterDrawing', () => {
                if(savedView){
                    network.moveTo({position: savedView.position, scale: savedView.scale, animation: false});
                }
                // Use requestAnimationFrame to ensure the view is fully updated before showing
                requestAnimationFrame(() => container.classList.add('show'));
            });
            network.on("dragEnd", p => {
                if(p.nodes.length){
                    const pos=network.getPositions(p.nodes);
                    p.nodes.forEach(id=>{ customPositions[id]={x:pos[id].x/distance, y:pos[id].y/distance}; basePositions[id]=customPositions[id]; });
                }
            });
        }
        
        init();
    </script>
</body>
</html>'''

class TGraphRequestHandler(SimpleHTTPRequestHandler):
    """Custom HTTP request handler for TGraph visualization"""
    
    # Class-level cache shared across all handler instances
    _cache = None
    _tgraph = None
    
    def __init__(self, tgraph, *args, **kwargs):
        # Initialize class-level cache only once
        if TGraphRequestHandler._tgraph is not tgraph:
            TGraphRequestHandler._tgraph = tgraph
            TGraphRequestHandler._cache = TGraphCache(tgraph, max_size=100)
            # print("[Server] Initialized new TGraph cache", flush=True)
        self.tgraph = tgraph
        self.cache = TGraphRequestHandler._cache
        super().__init__(*args, **kwargs)
    
    def do_GET(self):
        parsed_path = urllib.parse.urlparse(self.path)
        path = parsed_path.path
        
        if path == '/' or path == '/index.html':
            self._serve_html()
        elif path == '/api/time_structure':
            self._serve_time_structure()
        elif path == '/api/graph':
            self._serve_graph(parsed_path.query)
        else:
            self.send_error(404, 'Not Found')
    
    def _serve_html(self):
        html = _generate_html_template()
        self.send_response(200)
        self.send_header('Content-type', 'text/html')
        self.send_header('Content-Length', len(html.encode('utf-8')))
        self.end_headers()
        self.wfile.write(html.encode('utf-8'))
    
    def _serve_time_structure(self):
        structure = _get_time_index_structure(self.tgraph)
        response = json.dumps(structure)
        self.send_response(200)
        self.send_header('Content-type', 'application/json')
        self.send_header('Content-Length', len(response.encode('utf-8')))
        self.end_headers()
        self.wfile.write(response.encode('utf-8'))
    
    def _serve_graph(self, query_string):
        params = urllib.parse.parse_qs(query_string)
        mode = params.get('mode', ['cumulative'])[0]
        start = json.loads(params.get('start', ['null'])[0])
        end = json.loads(params.get('end', ['null'])[0])
        
        # print(f"[API] Request: mode={mode}, start={start}, end={end}", flush=True)
        
        # Use cache with lazy loading
        graph_data = self.cache.get_graph_json(mode, start, end)
        # print(f"[API] Result: {len(graph_data['nodes'])} nodes, {len(graph_data['edges'])} edges", flush=True)
        
        response = json.dumps(graph_data)
        self.send_response(200)
        self.send_header('Content-type', 'application/json')
        self.send_header('Content-Length', len(response.encode('utf-8')))
        self.end_headers()
        self.wfile.write(response.encode('utf-8'))
    
    def log_message(self, format, *args):
        # Suppress default logging
        pass


def tgraph_viz(tgraph, port=8050, open_browser=True, blocking=True):
    """
    Launch an interactive web visualization for a TGraph.
    
    This function starts a local web server that serves an interactive
    visualization interface. Users can:
    - Select time points using multi-axis sliders (one for each time index level)
    - Switch between cumulative and delta graph modes
    - View the graph at any selected time point
    
    Args:
        tgraph (TGraph): The temporal graph to visualize.
        port (int, optional): The port number for the web server. Defaults to 8050.
        open_browser (bool, optional): Whether to automatically open the browser. 
            Defaults to True.
        blocking (bool, optional): If True, blocks execution until stopped (best for scripts).
                                   If False, runs in a background thread (best for Jupyter).
                                   Defaults to True.
    
    Returns:
        HTTPServer: The running HTTP server instance.
    
    Example:
        >>> from ciga import TGraph, tgraph_viz
        >>> tg = TGraph(data=df, position=['Season', 'Episode', 'Scene'])
        >>> server = tgraph_viz(tg, port=8050)
        >>> # Visit http://localhost:8050 in your browser
        >>> # To stop: server.shutdown()
    
    Note:
        Press Ctrl+C in the terminal to stop the server, or call server.shutdown()
    """
    handler = partial(TGraphRequestHandler, tgraph)
    server = HTTPServer(('localhost', port), handler)
    
    url = f'http://localhost:{port}'
    print(f">> TGraph Visualization Server started at {url}", flush=True)

    if open_browser:
        threading.Timer(0.5, lambda: webbrowser.open(url)).start()

    def run_server():
        try:
            server.serve_forever()
        except KeyboardInterrupt:
            pass
        finally:
            server.server_close()
            print("\n>> Server stopped.", flush=True)

    if blocking:
        print("   Press Ctrl+C to stop the server", flush=True)
        run_server()
        return None
    else:
        print("   Server running in background thread.", flush=True)
        server_thread = threading.Thread(target=run_server, daemon=True)
        server_thread.start()
        return server