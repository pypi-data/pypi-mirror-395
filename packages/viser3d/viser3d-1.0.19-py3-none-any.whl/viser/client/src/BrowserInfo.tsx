import React, { useContext, useEffect } from "react";
import { detect } from "detect-browser";

import { BrowserInfoMessage } from "./WebsocketMessages";
import { ViewerContext } from "./ViewerContext";

/**
 * Hook that sends browser information to the server when the page has finished loading
 * and the websocket connection is established.
 */
export function useBrowserInfoMessage() {
  const viewer = useContext(ViewerContext)!;
  const viewerMutable = viewer.mutable.current;
  const server = viewer.useGui((state) => state.server);
  const connected = viewer.useGui((state) => state.websocketConnected);
  const pageLoaded = React.useRef(false);
  const hasSentBrowserInfo = React.useRef(false);

  const onPageLoad = () => {
    pageLoaded.current = true;
  };

  useEffect(() => {
    if (document.readyState === "complete") {
      pageLoaded.current = true;
    } else {
      window.addEventListener("load", onPageLoad);
    }

    return () => {
      window.removeEventListener("load", onPageLoad);
    };
  }, []);

  useEffect(() => {
    if (!server || !connected || !pageLoaded.current || hasSentBrowserInfo.current) return;

    const url = new URL(window.location.href);
    const searchParams: Record<string, string> = {};
    url.searchParams.forEach((value, key) => {
      searchParams[key] = value;
    });

    const browser = detect();

    const browserInfo: BrowserInfoMessage = {
      type: "BrowserInfoMessage",
      user_agent: navigator.userAgent,
      browser_name: browser?.name || "",
      browser_version: browser?.version || "",
      os_name: browser?.os || null,
      url: window.location.href,
      origin: window.location.origin,
      pathname: window.location.pathname,
      search_params: searchParams,
      screen_width: window.screen.width,
      screen_height: window.screen.height,
    };

    viewerMutable.sendMessage(browserInfo);
    hasSentBrowserInfo.current = true;
  }, [server, connected, pageLoaded]);
}
