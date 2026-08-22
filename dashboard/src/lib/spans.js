function timestampValue(value) {
  const timestamp = Date.parse(value);
  return Number.isNaN(timestamp) ? Number.POSITIVE_INFINITY : timestamp;
}

export function sortSpansByStart(spans) {
  return [...spans].sort((left, right) => {
    const leftTimestamp = timestampValue(left.started_at);
    const rightTimestamp = timestampValue(right.started_at);
    if (leftTimestamp !== rightTimestamp) return leftTimestamp - rightTimestamp;

    return String(left.span_id).localeCompare(String(right.span_id));
  });
}

function hasAncestryCycle(span, spansById) {
  const visited = new Set([span.span_id]);
  let parentId = span.parent_span_id;

  while (parentId && spansById.has(parentId)) {
    if (visited.has(parentId)) return true;

    visited.add(parentId);
    parentId = spansById.get(parentId).parent_span_id;
  }

  return false;
}

export function buildSpanTree(spans) {
  const sortedSpans = sortSpansByStart(spans);
  const spansById = new Map(
    sortedSpans.map((span) => [span.span_id, { ...span, children: [] }]),
  );
  const roots = [];

  for (const span of spansById.values()) {
    const parent = span.parent_span_id ? spansById.get(span.parent_span_id) : null;

    if (parent && !hasAncestryCycle(span, spansById)) {
      parent.children.push(span);
    } else {
      roots.push(span);
    }
  }

  for (const span of spansById.values()) {
    span.children = sortSpansByStart(span.children);
  }

  return sortSpansByStart(roots);
}
