// ⚠️ YOUR FIREBASE CONFIG
var firebaseConfig = {
  apiKey: "AIzaSyC1DNZDToGvgEy1AXADXvWfnbG-oc2o7nQ",
  authDomain: "bidyut-bazar.firebaseapp.com",
  projectId: "bidyut-bazar",
  storageBucket: "bidyut-bazar.firebasestorage.app",
  messagingSenderId: "558333225305",
  appId: "1:558333225305:web:0acd52172bdc0a27b10448",
  measurementId: "G-Q5YD8JC1VN"
};

firebase.initializeApp(firebaseConfig);
var db = firebase.firestore();
var auth = firebase.auth();

// ============ SAFE $ HELPER ============
function $(id) { return document.getElementById(id); }

// ============ FLASH MESSAGE ============
function flash(text, ok) {
  if (ok === undefined) ok = true;
  var msgBox = document.getElementById('msg');
  if (!msgBox) { alert(text); return; }
  var div = document.createElement('div');
  var icon = ok ? '<i class="fa-solid fa-circle-check"></i>' : '<i class="fa-solid fa-circle-xmark"></i>';
  div.className = 'msg ' + (ok ? 'msg-ok' : 'msg-err');
  div.innerHTML = icon + ' ' + text;
  msgBox.appendChild(div);
  setTimeout(function() { if (div.parentNode) div.parentNode.removeChild(div); }, 3500);
}

// ============ SET NAV ============
function setNav(name, batch) {
  var nav = document.getElementById('navRight');
  if (!nav) return;
  var batchHtml = '';
  if (batch) {
    var isHSC = batch === 'HSC';
    var isAdmin = batch === 'Admin';
    var bg = isAdmin ? 'rgba(255,255,255,0.25)' : isHSC ? 'rgba(168,85,247,0.3)' : 'rgba(255,255,255,0.2)';
    var icon = isAdmin ? 'fa-shield-halved' : isHSC ? 'fa-graduation-cap' : 'fa-school';
    batchHtml = '<span style="background:' + bg + ';color:white;padding:4px 10px;border-radius:20px;font-size:11.5px;font-weight:700;border:1px solid rgba(255,255,255,0.3);display:inline-flex;align-items:center;gap:5px;"><i class="fa-solid ' + icon + '"></i>' + batch + '</span>';
  }
  nav.innerHTML =
    '<span style="color:rgba(255,255,255,0.9);font-size:13px;display:inline-flex;align-items:center;gap:6px;"><i class="fa-solid fa-circle-user" style="font-size:15px;"></i> ' + name + '</span>' +
    batchHtml +
    '<button onclick="logout()" style="background:rgba(255,255,255,0.15);color:white;border:1px solid rgba(255,255,255,0.3);padding:7px 16px;border-radius:20px;cursor:pointer;font-size:12.5px;font-weight:600;font-family:inherit;display:inline-flex;align-items:center;gap:6px;transition:background 0.2s;" onmouseover="this.style.background=\'rgba(220,38,38,0.5)\'" onmouseout="this.style.background=\'rgba(255,255,255,0.15)\'"><i class="fa-solid fa-right-from-bracket"></i> Logout</button>';
}

// ============ CLEAR NAV ============
function clearNav() {
  var nav = document.getElementById('navRight');
  if (nav) nav.innerHTML = '';
}

// ============ LOGIN ============
function login() {
  var emailEl = document.getElementById('lEmail');
  var passEl = document.getElementById('lPass');
  if (!emailEl || !passEl) { flash('Form elements not found', false); return; }
  var email = emailEl.value.trim();
  var pass = passEl.value;
  if (!email || !pass) { flash('Fill all fields', false); return; }
  auth.signInWithEmailAndPassword(email, pass).catch(function(e) { flash(e.message, false); });
}

// ============ REGISTER ============
function register() {
  var nameEl = document.getElementById('rName');
  var emailEl = document.getElementById('rEmail');
  var passEl = document.getElementById('rPass');
  if (!nameEl || !emailEl || !passEl) { flash('Form elements not found', false); return; }
  var name = nameEl.value.trim();
  var email = emailEl.value.trim();
  var pass = passEl.value;
  if (!name || !email || !pass) { flash('Fill all fields', false); return; }
  if (pass.length < 6) { flash('Password must be at least 6 characters', false); return; }
  var batchEl = document.querySelector('input[name="batch"]:checked');
  var batch = batchEl ? batchEl.value : 'SSC';
  auth.createUserWithEmailAndPassword(email, pass)
    .then(function(cred) {
      return db.collection('users').doc(cred.user.uid).set({
        name: name, email: email, batch: batch, isAdmin: false, access: [],
        createdAt: firebase.firestore.FieldValue.serverTimestamp()
      });
    })
    .then(function() { flash('Account created! Welcome to ' + batch + ' batch!'); })
    .catch(function(e) { flash(e.message, false); });
}

// ============ LOGOUT ============
function logout() {
  auth.signOut().then(function() { window.location = 'index.html'; });
}

// ============ SHOW FORMS ============
function showReg() {
  var lf = document.getElementById('loginForm'), rf = document.getElementById('regForm');
  if (lf) lf.style.display = 'none';
  if (rf) rf.style.display = 'block';
}
function showLogin() {
  var rf = document.getElementById('regForm'), lf = document.getElementById('loginForm');
  if (rf) rf.style.display = 'none';
  if (lf) lf.style.display = 'block';
}

// ============ NEWSFEED ============
// Loads wrong MCQs from completed attempts and renders a scrolling ticker
function loadNewsfeed(containerId) {
  var container = document.getElementById(containerId);
  if (!container) return;

  // Fetch all attempts, quizzes, build wrong-question list
  db.collection('attempts').limit(50).get().then(function(attSnap) {
    if (attSnap.empty) { renderNewsfeedEmpty(container); return; }

    // Gather unique quiz IDs
    var quizIds = {};
    attSnap.docs.forEach(function(d) { quizIds[d.data().quizId] = true; });
    var uniqueIds = Object.keys(quizIds);

    var quizPromises = uniqueIds.map(function(qid) {
      return db.collection('quizzes').doc(qid).get();
    });

    Promise.all(quizPromises).then(function(quizDocs) {
      var quizMap = {};
      quizDocs.forEach(function(qd) {
        if (qd.exists) quizMap[qd.id] = qd.data();
      });

      // Build list of wrong questions with error counts
      var wrongMap = {}; // key: quizId+qId => { q, count, subject, quizTitle }
      attSnap.docs.forEach(function(d) {
        var att = d.data();
        var quiz = quizMap[att.quizId];
        if (!quiz) return;
        quiz.questions.forEach(function(q) {
          var ans = att.answers ? att.answers[q.id] : null;
          if (ans && ans !== q.correct) {
            var key = att.quizId + '__' + q.id;
            if (!wrongMap[key]) {
              wrongMap[key] = { q: q, count: 0, subject: quiz.subject || '', quizTitle: quiz.title, batch: quiz.batch || '' };
            }
            wrongMap[key].count++;
          }
        });
      });

      var wrongList = Object.values(wrongMap);
      // Sort by most-missed first
      wrongList.sort(function(a, b) { return b.count - a.count; });

      if (wrongList.length === 0) { renderNewsfeedEmpty(container); return; }

      // Render ticker
      renderNewsfeedTicker(container, wrongList);
    });
  }).catch(function(e) {
    console.error('Newsfeed error:', e);
    renderNewsfeedEmpty(container);
  });
}

function renderNewsfeedEmpty(container) {
  container.innerHTML =
    '<div class="newsfeed-header"><h2><i class="fa-solid fa-fire-flame-curved"></i> Common Mistakes</h2><span style="color:rgba(255,255,255,0.6);font-size:12px;">Live feed</span></div>' +
    '<div class="newsfeed-empty"><i class="fa-regular fa-face-smile" style="font-size:20px;margin-bottom:6px;display:block;"></i>No quiz attempts yet. Be the first!</div>';
}

function renderNewsfeedTicker(container, list) {
  var items = list.slice(0, 30); // max 30 items
  var itemsHtml = '';
  items.forEach(function(entry, idx) {
    var q = entry.q;
    var correctLetter = q.correct.toUpperCase();
    var correctText = q[q.correct] || '';
    var batchBadge = entry.batch ? '<span style="background:' + (entry.batch === 'HSC' ? 'rgba(168,85,247,0.2)' : 'rgba(59,111,212,0.2)') + ';color:' + (entry.batch === 'HSC' ? '#a855f7' : '#3b6fd4') + ';padding:1px 6px;border-radius:4px;font-size:10px;font-weight:700;">' + entry.batch + '</span> ' : '';
    itemsHtml +=
      '<div class="feed-item">' +
        '<span class="feed-num">' + (idx + 1) + '</span>' +
        '<div class="feed-content">' +
          '<div class="feed-q">' + q.text.substring(0, 100) + (q.text.length > 100 ? '…' : '') + '</div>' +
          (q.explanation
            ? '<div class="feed-explain"><i class="fa-solid fa-lightbulb"></i>' + q.explanation.substring(0, 90) + (q.explanation.length > 90 ? '…' : '') + '</div>'
            : '<div class="feed-explain" style="color:#64748b;"><i class="fa-solid fa-check-circle" style="color:#16a34a;"></i> Correct: <strong>' + correctLetter + '. ' + correctText.substring(0, 60) + '</strong></div>') +
          '<div class="feed-meta">' +
            batchBadge +
            (entry.subject ? '<i class="fa-solid fa-book-open"></i>' + entry.subject + ' &bull; ' : '') +
            '<i class="fa-solid fa-users"></i>' + entry.count + ' missed' +
          '</div>' +
        '</div>' +
      '</div>';
  });

  // Duplicate for seamless loop
  var trackHtml = itemsHtml + itemsHtml;

  container.innerHTML =
    '<div class="newsfeed-header">' +
      '<h2><i class="fa-solid fa-fire-flame-curved" style="color:#fb923c;"></i> Common Mistakes &amp; Explanations</h2>' +
      '<span style="color:rgba(255,255,255,0.6);font-size:12px;display:flex;align-items:center;gap:5px;"><i class="fa-solid fa-circle" style="color:#22c55e;font-size:8px;"></i>Live</span>' +
    '</div>' +
    '<div class="newsfeed-ticker"><div class="newsfeed-track">' + trackHtml + '</div></div>';
                                                                                                                                                         }
