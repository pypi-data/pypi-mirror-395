import * as esbuild from 'esbuild';
import { readFileSync, writeFileSync } from 'fs';
import { resolve, dirname } from 'path';
import { fileURLToPath } from 'url';

const __dirname = dirname(fileURLToPath(import.meta.url));

const isWatch = process.argv.includes('--watch');

const buildOptions = {
  entryPoints: ['src/cesiumjs_anywidget/js/index.js'],
  bundle: true,
  format: 'esm',
  outfile: 'src/cesiumjs_anywidget/index.js',
  platform: 'browser',
  target: 'es2020',
  logLevel: 'info',
  banner: {
    js: '// Generated bundle - DO NOT EDIT DIRECTLY. Edit files in src/cesiumjs_anywidget/js/ instead.\n'
  }
};

async function build() {
  try {
    if (isWatch) {
      console.log('👀 Watching for changes...');
      const ctx = await esbuild.context(buildOptions);
      await ctx.watch();
    } else {
      console.log('🔨 Building...');
      await esbuild.build(buildOptions);
      console.log('✅ Build complete!');
    }
  } catch (error) {
    console.error('❌ Build failed:', error);
    process.exit(1);
  }
}

build();
