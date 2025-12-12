function updateGraphTooltip(event, pos, item, previousIndex, tooltip, plot) {
  if (item) {
    if (previousIndex != item.dataIndex) {
      previousIndex = item.dataIndex;
      var plot_offset = plot.getPlotOffset();
      var offset = plot.offset();
      tooltip.find(".x").html(item.series.xaxis.tickFormatter(
        item.datapoint[0], item.series.xaxis));
      tooltip.find(".y").html(item.series.yaxis.options.axisLabel + " : " +
        item.datapoint[1]);
      tooltip.css("left", item.pageX - offset.left + plot_offset.left + 5
        + "px");
      tooltip.show();
      // query offsetHeight *after* making the tooltip visible
      tooltip.css("top", item.pageY - offset.top + plot_offset.top - 5
        - tooltip.prop("offsetHeight") + "px");
    }
  } else {
    if (previousIndex != null) {
      tooltip.hide();
      previousIndex = null;
    }
  }
  return previousIndex;
}

scale_map = {
  log100To0: [
    function (v) { return -Math.log(101 - v); },
    function (v) { return 101 - Math.exp(-v); }
  ],
  log0ToAny: [
    function (v) { return Math.log(v + 1); },
    function (v) { return Math.exp(v) - 1; }
  ]
}

function updateAxisTransform(axis) {
  if (axis != undefined) {
    transform_list = scale_map[axis.transform];
    if (transform_list == undefined) {
      return;
    }
    axis.transform = transform_list[0];
    axis.inverseTransform = transform_list[1];
  }
}

function renderGraph(container) {
  var container = $(container);
  var previousIndex = null;
  var tooltip = container.next(".tooltip");
  var options = $.parseJSON(container.attr("data-options"));
  updateAxisTransform(options.xaxis);
  updateAxisTransform(options.yaxis);
  var plot = $.plot(
    container,
    $.parseJSON(container.attr("data-points")),
    options
  );
  tooltip.detach();
  container.append(tooltip);
  container.bind("plothover", function (event, pos, item) {
    previousIndex = updateGraphTooltip(event, pos, item, previousIndex,
      tooltip, plot);
  });
}
function toggleGraph(node) {
  var container = $(node).parent().find(".container");
  // Note: toggling *after* rendering cause layout problems with flot.
  container.toggle();
  if (container.attr("data-rendered-marker") == null) {
    container.attr("data-rendered-marker", "rendered");
    container.find(".graph").each(function (i){renderGraph(this)});
  }
}
function hideGraph(node) {
  $(node).parent().hide();
}
$(function() {
  $(".graph:visible").each(function (i){renderGraph(this)});
  $(".hidden_graph .container").draggable();
});
