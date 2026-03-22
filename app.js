// ⚠️ YOUR FIREBASE CONFIG
const firebaseConfig = {
  apiKey: "AIzaSyC1DNZDToGvgEy1AXADXvWfnbG-oc2o7nQ",
  authDomain: "bidyut-bazar.firebaseapp.com",
  projectId: "bidyut-bazar",
  storageBucket: "bidyut-bazar.firebasestorage.app",
  messagingSenderId: "558333225305",
  appId: "1:558333225305:web:0acd52172bdc0a27b10448",
  measurementId: "G-Q5YD8JC1VN"
};

firebase.initializeApp(firebaseConfig);
const db = firebase.firestore();
const auth = firebase.auth();

const $ = id => document.getElementById(id);

function flash(text, ok = true) {
  const msg = $('msg');
  if (!msg) return alert(text);
  const div = document.createElement('div');
  div.className = 'msg ' + (ok ? 'msg-ok' : 'msg-err');
  div.textContent = text;
  msg.appendChild(div);
  setTimeout(() => div.remove(), 3000);
}

function setNav(name) {
  const nav = $('navRight');
  if (!nav) return;
  nav.innerHTML =
    `<span style="color:white;margin-right:10px;">👤 ${name}</span>
     <button onclick="logout()" style="background:#e74c3c;color:white;border:none;padding:8px 20px;border-radius:20px;">Logout</button>`;
}

function clearNav() {
  const nav = $('navRight');
  if (nav) nav.innerHTML = '';
}

async function login() {
  const email = $('lEmail').value.trim();
  const pass = $('lPass').value;
  if (!email || !pass) return flash('Fill all fields', false);

  try {
    await auth.signInWithEmailAndPassword(email, pass);
  } catch (e) {
    flash(e.message, false);
  }
}

async function register() {
  const name = $('rName').value.trim();
  const email = $('rEmail').value.trim();
  const pass = $('rPass').value;

  if (!name || !email || !pass) return flash('Fill all fields', false);
  if (pass.length < 6) return flash('Password must be at least 6 characters', false);

  try {
    const cred = await auth.createUserWithEmailAndPassword(email, pass);

    // ✅ UPDATED USER STRUCTURE
    await db.collection('users').doc(cred.user.uid).set({
      name: name,
      email: email,
      isAdmin: false,
      access: [] // 👈 IMPORTANT
    });

    flash('Account created!');
    window.location.reload();

  } catch (e) {
    flash(e.message, false);
  }
}

function logout() {
  auth.signOut().then(() => {
    window.location = 'index.html';
  });
}