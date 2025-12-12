const FILTER_MODES = {
  ALL: 'all',
  DECLINED: 'declined',
};

const state = {
  folder: null,
  allFiles: [],
  files: [],
  index: 0,
  viewer: null,
  filter: FILTER_MODES.ALL,
  hasResults: false,
  declinedCount: 0,
};

const defaultFolder = window.MOLSELECTOR_DEFAULT_FOLDER;
const folderPicker = window.MOLSELECTOR_FOLDER_PICKER || { available: true, reason: '' };

const folderForm = document.getElementById('folder-form');
const folderInput = document.getElementById('folder-input');
const folderStatus = document.getElementById('folder-status');
const viewerSection = document.getElementById('viewer-section');
const viewerCanvas = document.getElementById('viewer');
const fileNameEl = document.getElementById('file-name');
const progressEl = document.getElementById('progress-bar');
const decisionStatus = document.getElementById('decision-status');
const acceptBtn = document.getElementById('accept-btn');
const declineBtn = document.getElementById('decline-btn');
const browseBtn = document.getElementById('browse-button');
const backBtn = document.getElementById('back-btn');
const declinedFilter = document.getElementById('declined-filter');
const declinedToggle = document.getElementById('declined-toggle');
const declinedCount = document.getElementById('declined-count');

function initViewer() {
  state.viewer = $3Dmol.createViewer(viewerCanvas, { backgroundColor: 'white' });
}

async function handleSetFolder(event) {
  event.preventDefault();
  const folderPath = folderInput.value.trim();
  if (!folderPath) {
    return;
  }
  await loadFolder(folderPath);
}

async function loadFolder(folderPath) {
  folderStatus.textContent = 'Loading folder…';
  try {
    const response = await fetch('/api/folder', {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({ folder: folderPath }),
    });
    if (!response.ok) {
      const error = await response.json().catch(() => ({ detail: response.statusText }));
      throw new Error(error.detail || 'Failed to load folder');
    }
    const data = await response.json();
    state.folder = data.folder;
    state.allFiles = data.files;
    state.hasResults = Boolean(data.has_results);
    state.filter = FILTER_MODES.ALL;
    rebuildFiles({ resetIndex: true });
    folderStatus.textContent = `Loaded ${state.allFiles.length} molecules from ${data.folder}`;
    viewerSection.classList.remove('hidden');
    updateViewer();
  } catch (error) {
    folderStatus.textContent = error.message;
    viewerSection.classList.add('hidden');
    state.folder = null;
    state.allFiles = [];
    state.hasResults = false;
    state.filter = FILTER_MODES.ALL;
    rebuildFiles({ resetIndex: true });
    setControlsEnabled(false);
    setBackEnabled(false);
  }
}

async function handleBrowse() {
  if (!folderPicker.available) {
    setManualEntryMessage(folderPicker.reason);
    return;
  }

  folderStatus.textContent = 'Opening folder picker…';
  try {
    const response = await fetch('/api/folder/picker');
    if (!response.ok) {
      const error = await response.json().catch(() => ({ detail: response.statusText }));
      throw new Error(error.detail || 'Failed to open folder picker');
    }
    const data = await response.json();
    folderInput.value = data.folder;
    await loadFolder(data.folder);
  } catch (error) {
    setManualEntryMessage(error.message);
    if (!state.folder) {
      setControlsEnabled(false);
      setBackEnabled(false);
    }
  }
}

function rebuildFiles(options = {}) {
  const { preferredPath = null, resetIndex = false } = options;
  const declinedFiles = state.allFiles.filter((file) => file.decision === 'decline');

  state.declinedCount = declinedFiles.length;
  state.files = state.filter === FILTER_MODES.DECLINED ? declinedFiles : [...state.allFiles];

  updateFilterControls();

  if (!state.files.length) {
    state.index = 0;
    setProgress();
    return;
  }

  if (resetIndex) {
    state.index = state.filter === FILTER_MODES.DECLINED ? 0 : findNextIndex(0);
  } else if (preferredPath) {
    const retainedIndex = state.files.findIndex((file) => file.path === preferredPath);
    if (retainedIndex !== -1) {
      state.index = retainedIndex;
    } else if (state.index >= state.files.length) {
      state.index = state.files.length - 1;
    }
  } else if (state.index >= state.files.length) {
    state.index = state.files.length - 1;
  }

  setProgress();
}

function updateFilterControls() {
  if (!declinedFilter || !declinedToggle || !declinedCount) {
    return;
  }

  const shouldShow = state.hasResults || state.declinedCount > 0;
  declinedFilter.classList.toggle('hidden', !shouldShow);
  declinedCount.textContent = `${state.declinedCount} declined`;
  declinedToggle.checked = state.filter === FILTER_MODES.DECLINED;
  declinedToggle.disabled = state.declinedCount === 0;
}

function findNextIndex(start) {
  if (!state.files.length) {
    return 0;
  }
  for (let i = start; i < state.files.length; i += 1) {
    if (!state.files[i].decision) {
      return i;
    }
  }
  return Math.min(start, state.files.length - 1);
}

async function updateViewer() {
  setProgress();

  if (!state.files.length) {
    fileNameEl.textContent = 'No molecules to display';
    decisionStatus.textContent =
      state.filter === FILTER_MODES.DECLINED
        ? 'No declined molecules to review in this folder.'
        : '';
    if (state.viewer) {
      state.viewer.clear();
      state.viewer.render();
    }
    setControlsEnabled(false);
    setBackEnabled(false);
    return;
  }

  const file = state.files[state.index];
  decisionStatus.textContent = file.decision ? `Already marked as ${file.decision}` : '';
  if (state.filter === FILTER_MODES.DECLINED && !decisionStatus.textContent) {
    decisionStatus.textContent = 'Reviewing previously declined molecules.';
  }
  fileNameEl.textContent = file.name;
  setControlsEnabled(true);
  setBackEnabled(state.index > 0);

  try {
    const response = await fetch(`/api/molecule?path=${encodeURIComponent(file.path)}`);
    if (!response.ok) {
      throw new Error('Unable to load molecule');
    }
    const data = await response.json();
    renderMolecule(data);
  } catch (error) {
    decisionStatus.textContent = error.message;
  }
}

function renderMolecule({ content, format }) {
  state.viewer.clear();
  state.viewer.resize();
  try {
    state.viewer.addModel(content, format);
    state.viewer.setStyle({}, { stick: { radius: 0.15 }, sphere: { scale: 0.18 } });
    state.viewer.zoomTo();
    state.viewer.render();
  } catch (error) {
    decisionStatus.textContent = 'Failed to visualize molecule';
  }
}

async function submitDecision(decision) {
  if (!state.files.length) {
    return;
  }
  const file = state.files[state.index];
  decisionStatus.textContent = `${decision === 'accept' ? 'Accepting' : 'Declining'} ${file.name}…`;

  try {
    const response = await fetch('/api/decision', {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({ path: file.path, decision }),
    });

    if (!response.ok) {
      const error = await response.json().catch(() => ({ detail: response.statusText }));
      throw new Error(error.detail || 'Failed to save decision');
    }

    updateLocalDecision(file.path, decision);
    rebuildFiles({ preferredPath: file.path });
    decisionStatus.textContent = `Marked ${file.name} as ${decision}.`;
    const stillVisible = state.files.some((item) => item.path === file.path);
    const stayOnCurrent = state.filter === FILTER_MODES.DECLINED && !stillVisible;
    advance({ stayOnCurrent });
  } catch (error) {
    decisionStatus.textContent = error.message;
  }
}

function updateLocalDecision(path, decision) {
  state.allFiles = state.allFiles.map((file) => (file.path === path ? { ...file, decision } : file));
}

function advance(options = {}) {
  const { stayOnCurrent = false } = options;

  if (!state.files.length) {
    updateViewer();
    setControlsEnabled(false);
    setBackEnabled(false);
    return;
  }

  if (state.filter === FILTER_MODES.DECLINED) {
    if (stayOnCurrent) {
      updateViewer();
      return;
    }

    const nextIndex = state.index + 1;
    if (nextIndex >= state.files.length) {
      setProgress();
      decisionStatus.textContent += ' No more declined molecules.';
      setControlsEnabled(true);
      setBackEnabled(state.files.length > 1);
      return;
    }
    state.index = nextIndex;
    updateViewer();
    return;
  }

  const nextIndex = findNextUnmarked(state.index + 1);
  if (nextIndex === null) {
    setProgress();
    decisionStatus.textContent += ' All molecules reviewed.';
    setControlsEnabled(true);
    setBackEnabled(state.files.length > 1);
    return;
  }
  state.index = nextIndex;
  updateViewer();
}

function goToPrevious() {
  if (!state.files.length) {
    return;
  }
  if (state.index === 0) {
    decisionStatus.textContent = 'Already at the first molecule.';
    return;
  }
  state.index -= 1;
  updateViewer();
}

function findNextUnmarked(start) {
  for (let i = start; i < state.files.length; i += 1) {
    if (!state.files[i].decision) {
      return i;
    }
  }
  const firstPending = state.files.findIndex((file) => !file.decision);
  return firstPending === -1 ? null : firstPending;
}

function setProgress() {
  if (!state.files.length) {
    progressEl.textContent = '0 / 0';
    return;
  }

  if (state.filter === FILTER_MODES.DECLINED) {
    progressEl.textContent = `${state.index + 1} / ${state.files.length} declined`;
    return;
  }

  const reviewed = state.files.filter((file) => file.decision).length;
  progressEl.textContent = `${reviewed} / ${state.files.length}`;
}

function setControlsEnabled(enabled) {
  acceptBtn.disabled = !enabled;
  declineBtn.disabled = !enabled;
  acceptBtn.classList.toggle('disabled', !enabled);
  declineBtn.classList.toggle('disabled', !enabled);
}

function setBackEnabled(enabled) {
  backBtn.disabled = !enabled;
  backBtn.classList.toggle('disabled', !enabled);
}

function handleDeclinedToggle(event) {
  const useDeclinedOnly = Boolean(event.target.checked);
  state.filter = useDeclinedOnly ? FILTER_MODES.DECLINED : FILTER_MODES.ALL;
  rebuildFiles({ resetIndex: true });
  decisionStatus.textContent = useDeclinedOnly
    ? 'Viewing only molecules previously marked as declined.'
    : 'Showing all molecules.';
  updateViewer();
}

function initBrowseSupport() {
  if (!folderPicker.available) {
    browseBtn.disabled = true;
    browseBtn.classList.add('disabled');
    setManualEntryMessage(folderPicker.reason);
  }
}

function setManualEntryMessage(reason) {
  const guidance = 'Folder picker is unavailable; enter a folder path manually and click Load Folder.';
  if (!reason) {
    folderStatus.textContent = guidance;
    return;
  }
  const separator = reason.trim().endsWith('.') ? ' ' : '. ';
  folderStatus.textContent = `${reason}${separator}${guidance}`;
}

folderForm.addEventListener('submit', handleSetFolder);
acceptBtn.addEventListener('click', () => submitDecision('accept'));
declineBtn.addEventListener('click', () => submitDecision('decline'));
browseBtn.addEventListener('click', handleBrowse);
backBtn.addEventListener('click', goToPrevious);
if (declinedToggle) {
  declinedToggle.addEventListener('change', handleDeclinedToggle);
}
document.addEventListener('keydown', handleKeydown);
window.addEventListener('resize', () => {
  if (state.viewer) {
    state.viewer.resize();
    state.viewer.render();
  }
});

initBrowseSupport();
initViewer();
updateFilterControls();

if (typeof defaultFolder === 'string' && defaultFolder.trim()) {
  folderInput.value = defaultFolder;
  void loadFolder(defaultFolder);
}

function handleKeydown(event) {
  if (!state.files.length) {
    return;
  }

  const activeTag = (event.target && event.target.tagName) || '';
  if (['INPUT', 'TEXTAREA', 'SELECT'].includes(activeTag) || (event.target && event.target.isContentEditable)) {
    return;
  }

  switch (event.key) {
    case 'ArrowRight':
    case 'Enter':
    case 'a':
    case 'A': {
      if (!acceptBtn.disabled) {
        event.preventDefault();
        submitDecision('accept');
      }
      break;
    }
    case 'ArrowLeft':
    case 'd':
    case 'D': {
      if (!declineBtn.disabled) {
        event.preventDefault();
        submitDecision('decline');
      }
      break;
    }
    case 'ArrowUp':
    case 'Backspace':
    case 'b':
    case 'B': {
      if (!backBtn.disabled) {
        event.preventDefault();
        goToPrevious();
      }
      break;
    }
    default:
      break;
  }
}
