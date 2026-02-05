
links = {}
ids = {}

function Div(el)
  text = pandoc.utils.stringify(el.content)
  ids[el.identifier] = text
end

function Header(el)
  text = pandoc.utils.stringify(el.content)
  ids[el.identifier] = text
end

function Link(el)
  text = pandoc.utils.stringify(el.content)
  if(el.target~="") then
    links[el.target] = text
  else
    links[text] = text
  end
end

function Pandoc(doc)
  for ref,ltext in pairs(links) do
    if(string.sub(ref,1,1)=="#") then
      rid = string.sub(ref,2)
      bid=0
      for id,htext in pairs(ids) do
        --       io.stderr:write("[Debug] id: "..id.."ref: "..rid)
        if (rid==id) then
          bid=1
          if(htext~=ltext) then
            io.stderr:write("[Warning] link text ["..ltext.."] doesn't match heading text ["..htext.."] for ref "..id,"\n")
          end
        end
      end
      if(bid==0) then
        io.stderr:write("[Warning] No identifier for ref "..ref,"\n")
      end
    end
  end
  return pandoc.Pandoc(doc.blocks,doc.meta)
end
