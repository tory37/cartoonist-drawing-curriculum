import { initializeApp } from "https://www.gstatic.com/firebasejs/12.17.1/firebase-app.js";
import {
  getAuth, GoogleAuthProvider, signInWithCredential, signOut, onAuthStateChanged
} from "https://www.gstatic.com/firebasejs/12.17.1/firebase-auth.js";
import {
  getFirestore, doc, setDoc, onSnapshot
} from "https://www.gstatic.com/firebasejs/12.17.1/firebase-firestore.js";

var schema = window.PROGRESS_SCHEMA || {};
var pageId = document.body.getAttribute("data-page-id") || null;

var signinBtn = document.getElementById("signin-btn");
var signoutBtn = document.getElementById("signout-btn");
var authUserEl = document.getElementById("auth-user");
var headerProgressEl = document.getElementById("header-progress");
var trackerNote = document.getElementById("tracker-note");

function totalForPage(pid){ return (schema[pid] || []).length; }
function doneForPage(pid, data){
  var items = (data && data[pid]) || {};
  var n = 0;
  for (var k in items) { if (items[k]) n++; }
  return n;
}
function totalAll(){
  var t = 0;
  for (var pid in schema) t += schema[pid].length;
  return t;
}
function doneAll(data){
  var d = 0;
  for (var pid in schema) d += doneForPage(pid, data);
  return d;
}

function renderChecklist(data){
  if (!pageId) return;
  var items = (data && data[pageId]) || {};
  var boxes = document.querySelectorAll(".track-item input[type=checkbox]");
  for (var i = 0; i < boxes.length; i++){
    var cb = boxes[i];
    cb.checked = !!items[cb.getAttribute("data-id")];
  }
}

function renderProgress(data){
  var total = totalAll(), done = doneAll(data || {});
  if (headerProgressEl){
    headerProgressEl.textContent = total ? (done + "/" + total + " tracked") : "";
    headerProgressEl.style.display = total ? "inline-block" : "none";
  }
  var bar = document.getElementById("overall-progress");
  if (bar){
    var pct = total ? Math.round((done / total) * 100) : 0;
    bar.querySelector(".bar-fill").style.width = pct + "%";
    bar.querySelector(".bar-label").textContent = done + "/" + total + " exercises tracked (" + pct + "%)";
  }
  var pills = document.querySelectorAll("[data-progress-for]");
  for (var i = 0; i < pills.length; i++){
    var node = pills[i];
    var pid = node.getAttribute("data-progress-for");
    var t = totalForPage(pid), d = doneForPage(pid, data || {});
    node.textContent = t ? (d + "/" + t) : "";
    node.classList.toggle("complete", t > 0 && d === t);
  }
}

function renderContinue(data, signedIn){
  var card = document.getElementById("continue-card");
  if (!card) return;
  var pages = window.PAGE_INFO || [];
  if (!signedIn || doneAll(data || {}) === 0){
    card.style.display = "none";
    return;
  }
  var target = null;
  for (var i = 0; i < pages.length; i++){
    var p = pages[i];
    if (doneForPage(p.id, data || {}) < totalForPage(p.id)){ target = p; break; }
  }
  if (!target){
    card.style.display = "none";
    return;
  }
  var link = document.getElementById("continue-link");
  var titleEl = link.querySelector(".continue-title");
  titleEl.innerHTML = target.title;
  link.setAttribute("href", target.file);
  card.style.display = "";
}

function setSignedInUI(user){
  if (user){
    if (signinBtn) signinBtn.style.display = "none";
    if (signoutBtn) signoutBtn.style.display = "";
    if (authUserEl){
      authUserEl.style.display = "";
      authUserEl.textContent = user.displayName ? user.displayName.split(" ")[0] : "Signed in";
    }
  } else {
    if (signinBtn) signinBtn.style.display = "";
    if (signoutBtn) signoutBtn.style.display = "none";
    if (authUserEl) authUserEl.style.display = "none";
  }
  var boxes = document.querySelectorAll(".track-item input[type=checkbox]");
  for (var i = 0; i < boxes.length; i++) boxes[i].disabled = !user;
  if (trackerNote) trackerNote.style.display = user ? "none" : "";
}

var cfg = window.FIREBASE_CONFIG;
var configured = cfg && cfg.apiKey && cfg.apiKey.indexOf("PASTE") === -1;

if (!configured){
  setSignedInUI(null);
  renderProgress({});
  renderContinue({}, false);
  if (signinBtn) signinBtn.textContent = "Tracking not set up yet";
  if (trackerNote) trackerNote.textContent = "Progress tracking isn\u2019t connected yet \u2014 see the setup steps to enable it.";
} else {
  var app = initializeApp(cfg);
  var auth = getAuth(app);
  var db = getFirestore(app);
  var unsub = null;

  // Firebase's own popup/redirect sign-in depends on a storage/iframe relay
  // between this site's own domain and the Firebase authDomain (a
  // different origin) to complete. Modern mobile browsers increasingly
  // block that relay as third-party tracking protection (Safari's ITP,
  // Firefox's Total Cookie Protection, etc.), so it fails silently: it
  // looks like it worked, but the result never comes back. Google Identity
  // Services talks to accounts.google.com directly instead (first-party,
  // no relay needed) and hands back an ID token, which we exchange for a
  // Firebase session in one direct call.
  function handleGoogleCredential(response){
    var cred = GoogleAuthProvider.credential(response.credential);
    signInWithCredential(auth, cred).catch(function(e){
      console.error("sign-in failed:", e);
      if (trackerNote){
        trackerNote.style.display = "";
        trackerNote.textContent = "Sign-in didn\u2019t go through (" + e.code + "). Please try again.";
      }
    });
  }

  var gsi = window.google && window.google.accounts && window.google.accounts.id;
  if (signinBtn && gsi && cfg.googleClientId && cfg.googleClientId.indexOf("PASTE") === -1){
    gsi.initialize({
      client_id: cfg.googleClientId,
      callback: handleGoogleCredential,
      auto_select: false
    });
    gsi.renderButton(signinBtn, { theme: "filled_black", shape: "pill", size: "medium", text: "signin_with" });
  }

  if (signoutBtn) signoutBtn.addEventListener("click", function(){
    signOut(auth);
    if (gsi) gsi.disableAutoSelect();
  });

  var boxes = document.querySelectorAll(".track-item input[type=checkbox]");
  for (var i = 0; i < boxes.length; i++){
    (function(cb){
      cb.addEventListener("change", function(){
        if (!auth.currentUser || !pageId) return;
        var id = cb.getAttribute("data-id");
        var field = pageId + "." + id;
        var payload = {};
        payload[pageId] = {};
        payload[pageId][id] = cb.checked;
        payload.updatedAt = Date.now();
        setDoc(doc(db, "progress", auth.currentUser.uid), payload, { mergeFields: [field, "updatedAt"] })
          .catch(function(e){ console.error("write failed:", e); cb.checked = !cb.checked; });
      });
    })(boxes[i]);
  }

  onAuthStateChanged(auth, function(user){
    setSignedInUI(user);
    if (unsub){ unsub(); unsub = null; }
    if (user){
      unsub = onSnapshot(doc(db, "progress", user.uid), function(snap){
        var data = snap.data() || {};
        renderChecklist(data);
        renderProgress(data);
        renderContinue(data, true);
      });
    } else {
      renderChecklist({});
      renderProgress({});
      renderContinue({}, false);
    }
  });
}
