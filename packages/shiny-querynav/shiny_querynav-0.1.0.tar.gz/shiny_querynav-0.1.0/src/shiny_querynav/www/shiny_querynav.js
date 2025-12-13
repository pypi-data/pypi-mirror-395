Shiny.addCustomMessageHandler("queryNav", function (msg) {

  const url = new URL(window.location.href);
  const params = url.searchParams;

  if (!msg.value) {
    params.delete(msg.name);
  } else {
    params.set(msg.name, msg.value);
  }

  url.search = params.toString();
  window.history.replaceState(null, "", url.toString());
});
