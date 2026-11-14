import { test, expect } from '@playwright/test';

const ODAS = ['oda-01', 'oda-02', 'oda-03', 'oda-04'];
const ABAS = ['objetivo', 'conceitos', 'laboratorio', 'verificacao'];

function vigiarErros(page) {
  const erros = [];
  page.on('pageerror', (e) => erros.push(e.message));
  return erros;
}

for (const oda of ODAS) {
  test(`${oda}: quatro abas e nenhum bloco com erro`, async ({ page }) => {
    const erros = vigiarErros(page);
    await page.goto(`/${oda}/`);
    const abas = page.getByRole('tab');
    await expect(abas).toHaveCount(4);
    for (let i = 0; i < 4; i += 1) await abas.nth(i).click();
    await expect(page.locator('.bloco-erro')).toHaveCount(0);
    expect(erros).toEqual([]);
  });

  test(`${oda}: sem rolagem horizontal em 360 px`, async ({ page }) => {
    await page.setViewportSize({ width: 360, height: 800 });
    for (const aba of ABAS) {
      await page.goto(`/${oda}/#${aba}`);
      await expect(page.getByRole('tab')).toHaveCount(4);
      expect(await page.evaluate(() => document.documentElement.scrollWidth)).toBeLessThanOrEqual(360);
    }
  });
}

test('oda-01: o terminal simulado reproduz o 409 da agenda', async ({ page }) => {
  await page.goto('/oda-01/#laboratorio');
  const painel = page.locator('#painel-laboratorio');
  const campo = painel.getByLabel('Digite um comando').first();
  await campo.fill('python3 main.py');
  await campo.press('Enter');
  await expect(painel.locator('.terminal__tela').first()).toContainText('HTTP 409 CONFLICT');
});

test('oda-03: o terminal simulado reproduz o NOT_FOUND do gRPC', async ({ page }) => {
  await page.goto('/oda-03/#laboratorio');
  const painel = page.locator('#painel-laboratorio');
  const campo = painel.getByLabel('Digite um comando').nth(1);
  await campo.fill('python demo.py');
  await campo.press('Enter');
  await expect(painel.locator('.terminal__tela').nth(1)).toContainText('NOT_FOUND');
});

for (const oda of ['oda-03', 'oda-04']) {
  test(`${oda}: os diagramas da aba Conceitos viram SVG`, async ({ page }) => {
    await page.goto(`/${oda}/#conceitos`);
    const painel = page.locator('#painel-conceitos');
    await expect(painel.locator('.diagrama__area svg')).toHaveCount(1, { timeout: 15000 });
    await expect(painel.locator('.bloco-erro')).toHaveCount(0);
  });
}
