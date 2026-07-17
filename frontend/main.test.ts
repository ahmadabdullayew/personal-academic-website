import { afterEach, describe, expect, it, vi } from 'vitest';

import { markDocumentReady } from '../src/static_src/main';

describe('progressive enhancement bootstrap', () => {
  afterEach(() => {
    vi.unstubAllGlobals();
  });

  it('records readiness without replacing server-rendered content', () => {
    const root = { dataset: {} } as HTMLElement;

    markDocumentReady(root);

    expect(root.dataset.enhancements).toBe('ready');
  });

  it('marks the real document root when the browser module starts', async () => {
    const root = { dataset: {} } as HTMLElement;
    vi.stubGlobal('document', { documentElement: root });
    vi.resetModules();

    await import('../src/static_src/main');

    expect(root.dataset.enhancements).toBe('ready');
  });
});
