
links = {}
headers = {}

function Header(el)
  text = pandoc.utils.stringify(el.content)
  headers[el.identifier] = text
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
      id = string.sub(ref,2)

      bid=0
      btext=0
      for hid,htext in pairs(headers) do
        if (hid == id) then
          bid=1
          --if(htext~=ltext and ltext~="To the top of this page") then
           -- io.stderr:write("WARNING: Link text doesn't match header text for ref ",id,"\n")
          --end
        end
      end
      if(bid==0) then
            io.stderr:write("[Error] No identifier for ref ",ref,"\n")
      end
    end
  end
  return pandoc.Pandoc(doc.blocks,doc.meta)
end
