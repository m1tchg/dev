
links = {}
heads = {}


function Header(el)
  text = pandoc.utils.stringify(el.content)
  heads["#"..el.identifier] = text
end

function Pandoc(doc)

  --check all the frags
  --get all the links and headers that have the same id

  pandoc.walk_block(pandoc.Div(doc.blocks), {Link = function(el)
    text = pandoc.utils.stringify(el.content)
    if(heads[el.target]) then
      if (heads[el.target] ~= text) then
        io.stderr:write("[Warning] link text doesn't match header text: ","\n")
        io.stderr:write("htext: ",heads[el.target],"\n")
        io.stderr:write("link text: ",text,"\n")
        end
      end
    end

})
end
