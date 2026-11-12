// Example code, written for this repository. A link-preview feature:
// a user pastes a URL, the server fetches it and returns the page title.
// The change under review added preview.js's route, shown second.

// ---- guard.js: registered as middleware for every /api route ----
// (This file predates the change. The first pass did not open it.)
const dns = require("dns/promises");
const net = require("net");

const ALLOWED_HOSTS = new Set(["blog.example.com", "docs.example.com"]);

function isPrivateIp(ip) {
  if (net.isIPv4(ip)) {
    const [a, b] = ip.split(".").map(Number);
    return (
      a === 10 || a === 127 || a === 0 ||
      (a === 172 && b >= 16 && b <= 31) ||
      (a === 192 && b === 168) ||
      (a === 169 && b === 254)
    );
  }
  return ip === "::1" || ip.startsWith("fe80:") || ip.startsWith("fc") || ip.startsWith("fd");
}

async function ssrfGuard(req, res, next) {
  const target = req.body && req.body.url;
  if (!target) return next();
  let parsed;
  try {
    parsed = new URL(target);
  } catch {
    return res.status(400).json({ error: "bad url" });
  }
  if (parsed.protocol !== "https:" || !ALLOWED_HOSTS.has(parsed.hostname)) {
    return res.status(400).json({ error: "host not allowed" });
  }
  const addrs = await dns.lookup(parsed.hostname, { all: true });
  if (addrs.some((a) => isPrivateIp(a.address))) {
    return res.status(400).json({ error: "private address" });
  }
  return next();
}

module.exports = { ssrfGuard };

// ---- preview.js: the new route added by this change ----
const express = require("express");
const router = express.Router();

router.post("/api/preview", async (req, res) => {
  const resp = await fetch(req.body.url, { redirect: "manual", timeout: 5000 });
  const html = await resp.text();
  const title = /<title>([^<]*)<\/title>/.exec(html);
  res.json({ title: title ? title[1] : "" });
});

module.exports = router;
