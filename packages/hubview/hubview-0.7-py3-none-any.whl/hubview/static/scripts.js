// Enhance code blocks with copy buttons
(function () {
  function addCopyButtons() {
    document.querySelectorAll('pre > code').forEach(function (code) {
      var pre = code.parentElement;
      if (pre.dataset.hasCopy) return;
      pre.dataset.hasCopy = "1";
      var btn = document.createElement('button');
      btn.className = 'btn copy-btn';
      btn.textContent = 'Copy';
      btn.style.position = 'absolute';
      btn.style.right = '1rem';
      btn.style.top = '1rem';
      btn.style.opacity = '0.7';
      btn.addEventListener('click', function () {
        navigator.clipboard.writeText(code.textContent).then(function () {
          btn.textContent = 'Copied!';
          setTimeout(function () { btn.textContent = 'Copy'; }, 1200);
        });
      });
      pre.style.position = 'relative';
      pre.appendChild(btn);
    });
  }
  document.addEventListener('DOMContentLoaded', addCopyButtons);
  // also run after Mermaid renders
  document.addEventListener('readystatechange', addCopyButtons);
})();


async function loadTree(path, container) {
  try {
    const res = await fetch(`/api/list?path=${encodeURIComponent(path || "")}`);
    const data = await res.json();
    if (data.error) { container.textContent = data.error; return; }

    const ul = document.createElement('ul');
    for (const item of data.items) {
      const li = document.createElement('li');
      li.dataset.path = item.path;  // 👈 tag each node with its logical path

      if (item.is_dir) {
        const caret = document.createElement('span'); caret.className = 'caret'; caret.textContent = '▸';
        const label = document.createElement('span'); label.className = 'node folder'; label.innerHTML = '📁 ' + item.name;
        label.prepend(caret);

        label.addEventListener('click', async () => {
          await toggleDirNode(li, item.path, caret);
        });

        li.appendChild(label);
      } else {
        const a = document.createElement('a');
        a.className = 'file';
        a.textContent = '📄 ' + item.name;
        a.href = `/view/${item.path}`;
        a.dataset.path = item.path;  // 👈 tag anchor too
        li.appendChild(a);
      }
      ul.appendChild(li);
    }
    container.appendChild(ul);
  } catch (e) {
    container.textContent = 'Failed to load tree: ' + e;
  }
}

async function toggleDirNode(li, path, caretEl) {
  if (li.classList.contains('open')) {
    li.classList.remove('open'); caretEl.textContent = '▸';
    const sub = li.querySelector(':scope > ul'); if (sub) sub.remove();
  } else {
    li.classList.add('open'); caretEl.textContent = '▾';
    if (!li.querySelector(':scope > ul')) {
      const sub = document.createElement('ul'); li.appendChild(sub);
      await loadTree(path, sub);
    }
  }
}

// Expand the tree to a given path like "dir/subdir/file.py"
async function expandTreeToPath(fullPath, isFile){
  const treeRoot = document.getElementById('tree');
  if(!treeRoot) return;
  const parts = (fullPath || "").split('/').filter(Boolean);
  if (parts.length === 0) return;

  // we expand dirs step-by-step; for files, we expand parent dir and then highlight the file
  const dirParts = isFile ? parts.slice(0, -1) : parts.slice(); 
  let currentContainer = treeRoot; // start at root UL container

  let cum = [];
  for (const seg of dirParts){
    cum.push(seg);
    const cumPath = cum.join('/');

    // find an li at the current level for this segment
    let li = findLiAtLevel(currentContainer, cumPath);
    if(!li){
      // if not found, maybe the parent isn't loaded yet; try to load children of parent
      const parentPath = cum.slice(0, -1).join('/');
      const parentLi = parentPath ? findLiByPath(treeRoot, parentPath) : null;
      if(parentLi){
        const caret = parentLi.querySelector('.caret') || document.createElement('span');
        await ensureDirExpanded(parentLi, parentPath, caret);
        // now try to find again at the newly loaded level
        li = findLiAtLevel(parentLi, cumPath);
      } else {
        // Root likely not loaded yet — load it
        if(!treeRoot.querySelector(':scope > ul')){ await loadTree("", treeRoot); }
        li = findLiAtLevel(treeRoot, cumPath);
      }
    }

    if(li){
      const caret = li.querySelector('.caret') || document.createElement('span');
      await ensureDirExpanded(li, cumPath, caret);
      // set next level container to the new <ul> under this li
      currentContainer = li.querySelector(':scope > ul') || currentContainer;
    }
  }

  // highlight active node
  if (isFile){
    const a = treeRoot.querySelector(`a.file[data-path="${CSS.escape(fullPath)}"]`);
    if(a){
      clearActive();
      a.classList.add('active');
      a.scrollIntoView({block:'center'});
    }
  } else {
    const li = treeRoot.querySelector(`li[data-path="${CSS.escape(parts.join('/'))}"] > .node.folder`);
    if(li){
      clearActive();
      li.classList.add('active');
      li.scrollIntoView({block:'center'});
    }
  }
}

function clearActive(){
  document.querySelectorAll('.tree .active').forEach(el => el.classList.remove('active'));
}

async function ensureDirExpanded(li, path, caretEl){
  if(!li.classList.contains('open')){
    li.classList.add('open'); if(caretEl) caretEl.textContent = '▾';
    // only load children once
    if(!li.querySelector(':scope > ul')){
      const sub = document.createElement('ul'); li.appendChild(sub);
      await loadTree(path, sub);
    }
  }
}

function findLiByPath(root, path){
  return root.querySelector(`li[data-path="${CSS.escape(path)}"]`);
}

function findLiAtLevel(container, path){
  // within container's immediate UL, find li with data-path
  return container.querySelector(`:scope > ul > li[data-path="${CSS.escape(path)}"]`);
}



document.addEventListener('DOMContentLoaded', async function(){
  const tree = document.getElementById('tree');
  if(tree){
    // ensure the root list exists
    if(!tree.querySelector(':scope > ul')){ await loadTree("", tree); }
    // now expand to the current page's path
    if (window.CURRENT_PATH !== undefined){
      await expandTreeToPath(window.CURRENT_PATH, !!window.CURRENT_IS_FILE);
    }
  }
});


// --------------- Script runner (args, logs, stop, refresh) ---------------
let currentJob = null;
let pollTimer = null;

async function startScript(path) {
  const argsInput = document.getElementById('script-args');
  const args = argsInput ? argsInput.value.split(' ').filter(x => x) : [];
  const res = await fetch(`/run-script/${path}`, {
    method: 'POST',
    headers: { 'Content-Type': 'application/json' },
    body: JSON.stringify({ args })
  });
  const data = await res.json();
  const out = document.getElementById('script-output');
  if (data.error) { out.textContent = 'Error: ' + data.error; return; }
  currentJob = data.job_id;
  localStorage.setItem('localhub_last_job', currentJob);
  const stopBtn = document.getElementById('stop-btn');
  if (stopBtn) stopBtn.style.display = 'inline-block';
  out.textContent = 'Started job ' + currentJob + '...';
  if (pollTimer) clearInterval(pollTimer);
  pollTimer = setInterval(checkJob, 1000);
}

async function checkJob() {
  if (!currentJob) return;
  const res = await fetch(`/job/${currentJob}`);
  const data = await res.json();
  const out = document.getElementById('script-output');
  if (data.error) { out.textContent = 'Error: ' + data.error; clearInterval(pollTimer); return; }
  let txt = '';
  txt += `Status: ${data.status}\n`;
  if (data.cmd) txt += `Cmd: ${data.cmd.join(' ')}\n`;
  if (data.started) txt += `Started: ${data.started}\n`;
  if (data.ended) txt += `Ended: ${data.ended}\n`;
  if (typeof data.returncode === 'number') txt += `Exit code: ${data.returncode}\n`;
  txt += '\n';
  if (data.stdout) txt += data.stdout;
  if (data.stderr) txt += '\n[stderr]\n' + data.stderr;
  out.textContent = txt;
  if (data.status !== 'running') {
    clearInterval(pollTimer);
    const stopBtn = document.getElementById('stop-btn');
    if (stopBtn) stopBtn.style.display = 'none';
    localStorage.removeItem('localhub_last_job');
  }
}

async function stopScript() {
  if (!currentJob) return;
  await fetch(`/stop/${currentJob}`, { method: 'POST' });
  await checkJob();
}

document.addEventListener('DOMContentLoaded', function () {
  const last = localStorage.getItem('localhub_last_job');
  if (last) {
    currentJob = last;
    pollTimer = setInterval(checkJob, 1000);
    const stopBtn = document.getElementById('stop-btn');
    if (stopBtn) stopBtn.style.display = 'inline-block';
  }
});

