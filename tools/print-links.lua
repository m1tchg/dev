
links = {}

function Link(el)
  text = pandoc.utils.stringify(el.content)
  if(el.target~="") then
    links[el.target] = text
  else
    links[text] = text
  end
end

function Pandoc(doc)
  for a,block in pairs(doc.blocks) do
  end
  io.stderr:write("[Warning] No identifier for ref "..ref,"\n")
  return pandoc.Pandoc(doc.blocks,doc.meta)
end
