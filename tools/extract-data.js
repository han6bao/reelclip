// Pulls the portfolio data (VIDEOS, MEDIA, WORK) out of index.html into JSON for the static SEO pages.
const fs = require('fs');
const html = fs.readFileSync(__dirname + '/../index.html', 'utf8');
const a = html.indexOf('  var VIDEOS = [');
const b = html.indexOf('  // Vertical reels');
const c = html.indexOf('  var WORK = [];');
const d = html.indexOf('\n', html.indexOf("WORK.push({industry:'music'", c));
const end = html.indexOf('});', d) + 3;
const code = html.slice(a, b) + '\n' +
  "function slugify(t){ return String(t).toLowerCase().replace(/[^a-z0-9]+/g,'-').replace(/^-+|-+$/g,''); }\n" +
  "function mediaUrl(m){ return (m.file && !m.vimeo && !m.drive && !m.id) ? m.file : m.drive ? 'https://drive.google.com/file/d/'+m.drive+'/view' : m.vimeo ? 'https://vimeo.com/'+m.vimeo : 'https://www.youtube.com/watch?v='+m.id; }\n" +
  html.slice(c, end) + '\nreturn {VIDEOS, MEDIA, WORK};';
const {VIDEOS, MEDIA, WORK} = new Function(code)();
function slugify(t){ return String(t).toLowerCase().replace(/[^a-z0-9]+/g,'-').replace(/^-+|-+$/g,''); }
const out = WORK.filter(w => w._v).map(w => {
  const v = w._v;
  return {
    slug: slugify((w._v.artist) + '-' + (w._v.song)),
    industry: w.industry, industryLabel: w.industryLabel || '', client: w.client, title: w.title, titleFirst: !!w.titleFirst,
    type: w.type, year: w.year || v.year || '', kind: v.kind || '',
    img: v.img || w.img || '', poster: v.poster || '', vimeo: v.vimeo || '', youtube: v.id || '', drive: v.drive || '', file: v.file || '',
    deliverables: v.deliverables || '', brief: v.brief || '', result: v.result || '', line: v.line || '',
    approach: v.approach || [], beats: (v.beats || []).map(x => ({title: x.title, text: x.text, img: x.img || ''})),
    scope: v.scope || [], creditList: v.creditList || [], aboutShort: v.aboutShort || '', about: v.about || [], aboutSections: v.aboutSections || [], facts: v.facts || {},
    stills: v.stills || [], stillAlts: v.stillAlts || [],
    films: (v.films || []).map(f => ({name: f.name, len: f.len, crew: f.crew, img: f.img || f.v.img, vimeo: f.v.vimeo}))
  };
});
fs.writeFileSync(__dirname + '/work.json', JSON.stringify(out, null, 1));
console.log(out.length, 'projects:', out.map(o => o.slug).join(', '));
