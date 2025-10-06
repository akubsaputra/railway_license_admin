async function api(path, method='GET', body=null, token=null){
  const headers = {};
  if(token) headers['Authorization'] = 'Bearer ' + token;
  if(body) headers['Content-Type'] = 'application/json';
  const res = await fetch(path, {method, headers, body: body ? JSON.stringify(body): undefined});
  return res;
}

document.getElementById('load').onclick = async () => {
  const token = document.getElementById('token').value.trim();
  if(!token){ alert('Masukkan token admin'); return; }
  const res = await api('/admin/users', 'GET', null, token);
  if(!res.ok){ alert('Gagal muat data: ' + res.status); return; }
  const data = await res.json();
  const tbody = document.getElementById('user-table'); tbody.innerHTML = '';
  Object.entries(data).forEach(([u,v]) => {
    const tr = document.createElement('tr');
    tr.innerHTML = `<td>${u}</td><td>${v.device || '-'}</td><td><button class='btn btn-sm btn-danger' data-user='${u}'>Hapus</button></td>`;
    tbody.appendChild(tr);
  });
  tbody.querySelectorAll('button').forEach(btn => {
    btn.onclick = async (e) => {
      const u = btn.getAttribute('data-user');
      if(!confirm('Hapus user '+u+'?')) return;
      const r = await api('/admin/remove', 'POST', {username: u}, token);
      if(r.ok){ alert('Dihapus'); document.getElementById('load').click(); }
      else { alert('Gagal hapus'); }
    }
  });
}

document.getElementById('add_btn').onclick = async () => {
  const token = document.getElementById('token').value.trim();
  const username = document.getElementById('new_user').value.trim();
  const pw = document.getElementById('new_pw').value.trim();
  const device = document.getElementById('new_device').value.trim();
  if(!token || !username || !pw){ alert('Token, username, dan password wajib'); return; }
  const r = await api('/admin/add', 'POST', {username, password: pw, device}, token);
  if(r.ok){ alert('User added'); document.getElementById('load').click(); }
  else { alert('Gagal tambah user'); }
}
