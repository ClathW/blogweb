import DOMPurify from 'dompurify'
import MarkdownIt from 'markdown-it'

const markdown = new MarkdownIt({
  html: false,
  linkify: true,
  breaks: true,
})

export function renderMarkdown(source = '') {
  return DOMPurify.sanitize(markdown.render(source || ''))
}

export function markdownToText(source = '') {
  const rendered = renderMarkdown(source)
  const container = document.createElement('div')
  container.innerHTML = rendered
  return container.textContent.replace(/\s+/g, ' ').trim()
}
