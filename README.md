# Code Shield 3.0

O site mantido est? em `smoggy-star/`: Astro, TypeScript e Tailwind CSS via Vite. O site est?tico anterior foi retirado ap?s a valida??o das dez rotas Astro.

Use Node.js >= 22.12.0. Para instalar e executar:

```powershell
npm.cmd --prefix smoggy-star ci
npm.cmd run dev -- --background
```

Abra a URL informada pelo Astro (normalmente http://localhost:4321). Os comandos da raiz delegam ? aplica??o correta.

```powershell
npm.cmd run build
npm.cmd run preview
npm.cmd run astro -- dev status
npm.cmd run astro -- dev logs
npm.cmd run astro -- dev stop
```

Se o servidor existente n?o foi iniciado em background, seus logs ficam no terminal original. N?o h? scripts de lint ou `check` definidos.

## Estrutura

```text
smoggy-star/
  src/
    components/
      layout/  Header, Footer, NavigationDrawer
      home/    BrandBanner, HeroSection, ServicesSection, PortfolioSection
      ui/      SocialIcons, ServiceIcon, VideoBackground
    layouts/   MainLayout.astro
    pages/     index, sobre, contato, servicos/index, servicos/[slug]
    data/      services.ts
    styles/    global, variables, components, header, home, pages, footer
  public/
    images/branding/
    images/portfolio/
    videos/
```

`variables.css` concentra a paleta. `global.css` importa os estilos e cont?m a prefer?ncia global de movimento reduzido. Cada arquivo restante possui os estilos da ?rea correspondente, incluindo seus breakpoints. A estrutura segue os componentes nativos e estilos descritos na [documenta??o Astro](https://docs.astro.build/en/basics/astro-components/) e no [guia de CSS](https://docs.astro.build/en/guides/styling/).

O v?deo Matrix deve estar em `public/videos/matrix-bg.mp4`, com poster em `public/videos/matrix-poster.jpg`. ? distinto de `hero-code-shield.mp4` e `code-shield-orbit.mp4`. O componente compartilhado usa uma camada fixa com opacidade de 20%, overlay escuro e cards opacos. Fontes dos tr?s v?deos s?o anexadas apenas quando movimento ? permitido; sem JavaScript ou com movimento reduzido, os posters continuam dispon?veis.

Instagram e Facebook mant?m os ?cones originais como indicadores: URLs oficiais ainda n?o foram fornecidas. WhatsApp permanece funcional.

Consulte [REFACTOR-REPORT.md](REFACTOR-REPORT.md) para invent?rio, valida??o e limita??es.
