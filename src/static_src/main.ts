import './styles/main.css';

export function markDocumentReady(root: HTMLElement): void {
  root.dataset.enhancements = 'ready';
}

if (typeof document !== 'undefined') {
  markDocumentReady(document.documentElement);
}
