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
function $(id) {
  return document.getElementById(id);
}

// ============ FLASH MESSAGE ============
function flash(text, ok) {
  if (ok === undefined) ok = true;
  var msgBox = document.getElementById('msg');
  if (!msgBox) { alert(text); return; }
  var div = document.createElement('div');
  div.className = 'msg ' + (ok ? 'msg-ok' : 'msg-err');
  div.textContent = text;
  msgBox.appendChild(div);
  setTimeout(function() {
    if (div.parentNode) div.parentNode.removeChild(div);
  }, 3000);
}

// ============ SET NAV ============
function setNav(name, batch) {
  var nav = document.getElementById('navRight');
  if (!nav) return;
  var batchHtml = '';
  if (batch) {
    var batchColor = batch === 'HSC' ? '#9c27b0' : '#4a90d9';
    batchHtml = '<span style="background:' + batchColor + ';color:white;padding:4px 10px;border-radius:12px;font-size:12px;font-weight:bold;margin-right:10px;">' + batch + '</span>';
  }
  nav.innerHTML =
    '<span style="color:white;margin-right:6px;">👤 ' + name + '</span>' +
    batchHtml +
    '<button onclick="logout()" style="background:#e74c3c;color:white;border:none;padding:8px 20px;border-radius:20px;cursor:pointer;">Logout</button>';
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
  
  auth.signInWithEmailAndPassword(email, pass).catch(function(e) {
    flash(e.message, false);
  });
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
  
  // Get selected batch
  var batchEl = document.querySelector('input[name="batch"]:checked');
  var batch = batchEl ? batchEl.value : 'SSC';
  
  auth.createUserWithEmailAndPassword(email, pass)
    .then(function(cred) {
      return db.collection('users').doc(cred.user.uid).set({
        name: name,
        email: email,
        batch: batch,
        isAdmin: false,
        access: [],
        createdAt: firebase.firestore.FieldValue.serverTimestamp()
      });
    })
    .then(function() {
      flash('Account created! Welcome to ' + batch + ' batch!');
      // DO NOT reload - onAuthStateChanged handles redirect
    })
    .catch(function(e) {
      flash(e.message, false);
    });
}

// ============ LOGOUT ============
function logout() {
  auth.signOut().then(function() {
    window.location = 'index.html';
  });
}

// ============ SHOW REGISTER / LOGIN FORMS ============
function showReg() {
  var loginForm = document.getElementById('loginForm');
  var regForm = document.getElementById('regForm');
  if (loginForm) loginForm.style.display = 'none';
  if (regForm) regForm.style.display = 'block';
}

function showLogin() {
  var regForm = document.getElementById('regForm');
  var loginForm = document.getElementById('loginForm');
  if (regForm) regForm.style.display = 'none';
  if (loginForm) loginForm.style.display = 'block';
}
