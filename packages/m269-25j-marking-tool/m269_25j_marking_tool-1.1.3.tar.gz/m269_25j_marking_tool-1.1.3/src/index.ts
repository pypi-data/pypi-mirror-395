import {
  JupyterFrontEnd,
  JupyterFrontEndPlugin
} from '@jupyterlab/application';
import { ICommandPalette } from '@jupyterlab/apputils';
import { INotebookTracker, NotebookPanel } from '@jupyterlab/notebook';
import { CodeCell, MarkdownCell } from '@jupyterlab/cells';
import { ContentsManager } from '@jupyterlab/services';
import { Contents } from '@jupyterlab/services';
import { PageConfig } from '@jupyterlab/coreutils';
import { showDialog, Dialog } from '@jupyterlab/apputils';
import { Widget } from '@lumino/widgets';
import { ISettingRegistry } from '@jupyterlab/settingregistry';
import { IDocumentManager } from '@jupyterlab/docmanager';

//import { IObservableJSON } from '@jupyterlab/observables';

/**
 * Initialization data for the m269-25j-marking-tool extension.
 */
const prep_command = 'm269-25j-marking-tool:prep';
const colourise_command = 'm269-25j-marking-tool:colourise';
const prep_for_students = 'm269-25j-marking-tool:prep_for_students';
const al_tests_command = 'm269-25j-prep-al-tests';
const open_all_tmas = 'm269-25j-marking-tool:open_all_tmas';
const finish_marking = 'm269-25j-marking-tool:finish_marking';

// Initial code cell code pt 1
const initial_code_cell_pt1 = `import pickle
from IPython.display import display, Markdown, HTML
import ipywidgets as widgets  # Ensure ipywidgets is imported

# Dictionary to store marks
pickle_file = "marks.dat"
try:
    with open(pickle_file, "rb") as f:
        question_marks = pickle.load(f)
except FileNotFoundError:
    print('Data file does not exist')`;

// Initial code cell code pt 2
const initial_code_cell_pt2 = `def on_radio_change(change, question_id, radio_widget):
    """React to radio button changes."""
    print('Radio change')
    print(change)
    question_marks[question_id]["awarded"] = change["new"]
    with open("marks.dat", "wb") as f:  # "wb" = write binary mode
        pickle.dump(question_marks, f)

def generate_radio_buttons(question_id):
    """Create radio buttons linked to stored_answers, updating a Markdown cell."""
    if question_id not in question_marks:
        raise ValueError(f"Question {question_id} not found in dictionary")
    previous_selection = question_marks[question_id].get("awarded")

    # Create radio buttons
    radio_buttons = widgets.RadioButtons(
        options=[key for key in question_marks[question_id].keys() if key != "awarded"],
        description="Grade:",
        disabled=False
    )
    if previous_selection is not None:
        radio_buttons.value = previous_selection  # Restore previous selection
    else:
        radio_buttons.value = None  # Ensure no selection
    # Attach event listener
    radio_buttons.observe(lambda change: on_radio_change(change, question_id,
    radio_buttons), names='value')

    # Display the radio buttons
    display(radio_buttons)


def create_summary_table():
    """Generate and display an HTML table from the question_marks dictionary."""
    if not question_marks:
        display(HTML("<p>No data available.</p>"))
        return

    # Start the HTML table with styling
    html = """
    <style>
        table {
            border-collapse: collapse;
            width: 100%;
            text-align: center;
        }
        th, td {
            border: 1px solid black;
            padding: 8px;
        }
        .not-selected {
            background-color: #ffcccc;
        }
    </style>
    <table>
        <tr>
            <th>Question</th>
            <th>Fail</th>
            <th>Pass</th>
            <th>Merit</th>
            <th>Distinction</th>
            <th>Awarded</th>
            <th>Marks</th>
        </tr>
    """

    total_marks = 0  # Sum of all selected marks

    # Loop through the dictionary to populate rows
    for question, values in question_marks.items():
        fail = values.get("fail", "-")
        passed = values.get("pass", "-")
        merit = values.get("merit", "-")
        distinction = values.get("distinction", "-")
        awarded = values.get("awarded", None)

        # If marked is None, highlight the cell
        awarded_display = awarded if awarded else "Not Awarded"
        awarded_class = "not-selected" if awarded is None else ""

        if awarded is not None:
            total_marks += values[awarded]  # Add to total
            marks = values[awarded]
        else:
            marks = 0

        html += f"""
        <tr>
            <td>{question}</td>
            <td>{fail}</td>
            <td>{passed}</td>
            <td>{merit}</td>
            <td>{distinction}</td>
            <td class='{awarded_class}'>{awarded_display}</td>
            <td>{marks}</td>
        </tr>
        """

    # Add total row
    html += f"""
    <tr>
        <td colspan='6'><b>Total Marks</b></td>
        <td><b>{total_marks}</b></td>
    </tr>
    """

    html += "</table>"
    # Display the table in the Jupyter Notebook
    display(HTML(html))`;

// Question Marks JSON
// TMA 01
const question_marks_tma01 = `    question_marks = {
        "Q1a": {"fail": 0, "pass": 2, "awarded": None},
        "Q1b": {"fail": 0, "pass": 2, "awarded": None},
        "Q1c": {"fail": 0, "pass": 2, "awarded": None},
        "Q2a": {"fail": 0, "pass": 3, "merit": 6, "distinction": 8, "awarded": None},
        "Q2bi": {"fail": 0, "pass": 5, "merit": 9, "distinction": 13, "awarded": None},
        "Q2bii": {"fail": 0, "pass": 2, "awarded": None},
        "Q2c": {"fail": 0, "pass": 3, "merit": 6, "distinction": 8, "awarded": None},
        "Q2d": {"fail": 0, "pass": 2, "merit": 3, "distinction": 5, "awarded": None},
        "Q3a": {"fail": 0, "pass": 4, "merit": 7, "distinction": 10, "awarded": None},
        "Q3b": {"fail": 0, "pass": 2, "awarded": None},
        "Q4a": {"fail": 0, "pass": 2, "merit": 4, "distinction": 6, "awarded": None},
        "Q4b": {"fail": 0, "pass": 2, "merit": 4, "awarded": None},
        "Q5a": {"fail": 0, "pass": 2, "merit": 4, "distinction": 6, "awarded": None},
        "Q5b": {"fail": 0, "pass": 3, "merit": 5, "distinction": 8, "awarded": None},
        "Q5c": {"fail": 0, "pass": 2, "merit": 4, "distinction": 6, "awarded": None},
        "Q6a": {"fail": 0, "pass": 4, "merit": 7, "distinction": 10, "awarded": None},
        "Q6b": {"fail": 0, "pass": 3, "merit": 6, "awarded": None},
    }`;
// TMA 02
const question_marks_tma02 = `    question_marks = {
        "Q1a": {"fail": 0, "pass": 2, "awarded": None},
        "Q1b": {"fail": 0, "pass": 2, "awarded": None},
        "Q1c": {"fail": 0, "pass": 2, "awarded": None},
        "Q2a": {"fail": 0, "pass": 3, "merit": 6, "distinction": 9, "awarded": None},
        "Q2b": {"fail": 0, "pass": 2, "merit": 4, "distinction": 6, "awarded": None},
        "Q2c": {"fail": 0, "pass": 2, "merit": 4, "distinction": 6, "awarded": None},
        "Q3a": {"fail": 0, "pass": 2, "merit": 4, "distinction": 6, "awarded": None},
        "Q3bi": {"fail": 0, "pass": 1, "merit": 3, "awarded": None},
        "Q3bii": {"fail": 0, "pass": 2, "merit": 4, "awarded": None},
        "Q4a": {"fail": 0, "pass": 2, "merit": 4, "distinction": 5, "awarded": None},
        "Q4bi": {"fail": 0, "pass": 1, "merit": 2, "distinction": 3, "awarded": None},
        "Q4bii": {"fail": 0, "pass": 1, "merit": 2, "awarded": None},
        "Q4biii": {"fail": 0, "pass": 6, "merit": 10, "distinction": 14,
         "awarded": None},
        "Q5a": {"fail": 0, "pass": 1, "merit": 2, "awarded": None},
        "Q5b": {"fail": 0, "pass": 1, "merit": 2, "awarded": None},
        "Q5c": {"fail": 0, "pass": 1, "merit": 2, "awarded": None},
        "Q5d": {"fail": 0, "pass": 1, "merit": 2, "awarded": None},
        "Q5e": {"fail": 0, "pass": 1, "merit": 2, "awarded": None},
        "Q5f": {"fail": 0, "pass": 1, "merit": 2, "awarded": None},
        "Q6a": {"fail": 0, "pass": 7, "merit": 12, "distinction": 16, "awarded": None},
        "Q6b": {"fail": 0, "pass": 2, "merit": 3, "distinction": 4, "awarded": None},
        "Q6c": {"fail": 0, "pass": 2, "merit": 4, "awarded": None},
    }`
// TMA 03
const question_marks_tma03 = `    question_marks = {
        "Q1a": {"fail": 0, "pass": 3, "merit": 5, "distinction": 7, "awarded": None},
        "Q1b": {"fail": 0, "pass": 3, "distinction": 6, "awarded": None},
        "Q1c": {"fail": 0, "pass": 2, "distinction": 5, "awarded": None},
        "Q1d": {"fail": 0, "pass": 2, "merit": 4, "distinction": 6, "awarded": None},
        "Q1e": {"fail": 0, "pass": 2, "merit": 4, "distinction": 6, "awarded": None},
        "Q2a": {"fail": 0, "pass": 2, "distinction": 4, "awarded": None},
        "Q2b": {"fail": 0, "pass": 3, "distinction": 6, "awarded": None},
        "Q2c": {"fail": 0, "pass": 4, "merit": 7, "distinction": 10, "awarded": None},
        "Q2d": {"fail": 0, "pass": 2, "merit": 3, "distinction": 4, "awarded": None},
        "Q2e": {"fail": 0, "pass": 2, "merit": 4, "distinction": 6, "awarded": None},
        "Q3a": {"fail": 0, "pass": 3, "awarded": None},
        "Q3b": {"fail": 0, "pass": 2, "merit": 4, "distinction": 6, "awarded": None},
        "Q4a": {"fail": 0, "pass": 2, "merit": 3, "distinction": 4, "awarded": None},
        "Q4b": {"fail": 0, "pass": 3, "merit": 6, "distinction": 8, "awarded": None},
        "Q4c": {"fail": 0, "pass": 3, "merit": 6, "distinction": 8, "awarded": None},
        "Q4d": {"fail": 0, "pass": 3, "merit": 6, "distinction": 8, "awarded": None},
        "Q5" : {"fail": 0, "pass": 3, "awarded": None},
    }`;

// Testing calls
const testCalls: Record<number, Record<string, string>> = {
  1: {
    'Q2bi' : `try: # allowed
    test(find_client_surname, al_test_table_tma01_q2bi)
except NameError:
    print('Function not defined.')`,
    'Q3a'  : `try: # allowed
    test(find_occurrences_with_follow_on, al_test_table_tma01_q3a)
except NameError:
    print('Function not defined.')`,
    'Q4a'  : `al_tests_tma01_q4a()`,
    'Q5b'  : `try: # allowed
    test(council_decision, al_test_table_tma01_q5b)
except NameError:
    print('Function not defined.')`,
    'Q6a'  : `try: # allowed
    test(weighted_council_decision, al_test_table_tma01_q6a)
except NameError:
    print('Function not defined.')`
  },
  2: {
    'Q2a'  : 'test(power, al_test_table_tma02_q2a)',
    'Q4biii' : 'al_test_tma02_q4biii()',
    'Q6a'  : 'al_test_tma02_q6a()'
  },
  3: {
    'Q1a'  : 'al_test_tma03_q1a()',
    'Q1d'  : 'al_test_tma03_q1d()',
    'Q2d'  : 'al_test_tma03_q2d()',
    'Q4d'  : 'al_tests_tma03_q4d()'
  }
};


// Walk through root dir looking for files
async function walkDir(
  contents: Contents.IManager,
  path: string,
  collected: string[] = []
): Promise<string[]> {
  const listing = await contents.get(path, { content: true });

  if (listing.type === 'directory' && listing.content) {
    for (const item of listing.content) {
      if (item.type === 'directory') {
        await walkDir(contents, item.path, collected);
      } else if (item.type === 'notebook' && item.path.endsWith('.ipynb')) {
        collected.push(item.path);
      }
    }
  }
  return collected;
}

function extractRadioValueFromRepr(repr: string): string | null {
  // 1. Extract the options list
  const optionsMatch = repr.match(/options=\(([^)]+)\)/);
  if (!optionsMatch) {
    console.log("No options match");
    return null;
  }

  const optionsRaw = optionsMatch[1]; // "'fail', 'pass', 'merit', 'distinction'"

  // Split on comma + whitespace between quoted strings
  const options = optionsRaw
    .split(/',\s*'|" ,\s*"/)
    .map(s => s.replace(/^['"]+|['"]+$/g, "").trim());

  // 2. Extract value= prefix
  const valueMatch = repr.match(/value\s*=\s*['"]([^'"]*)/);
  if (!valueMatch) {
    console.log("No value match");
    return null;
  }

  let prefix = valueMatch[1];

  // Remove every known ellipsis form
  prefix = prefix
    .replace(/\u2026/g, "")  // single char …
    .replace(/\.{3}/g, "")   // three dots
    .replace(/\s+$/g, "");   // trailing whitespace

  // 3. Find full match
  const full = options.find(o => o.startsWith(prefix));

  if (!full) {
    console.log("No option starts with:", prefix, "inside options:", options);
  }

  return full || null;
}

export async function decrypt(): Promise<string> {
  // Replace this with your encrypted base64-encoded string
  const ENCRYPTED_BASE64 = "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";
  const keyText = prompt("Enter 16-character decryption key:");
  if (!keyText || keyText.length !== 16) {
    throw new Error("Invalid key. Must be exactly 16 characters.");
  }

  const encryptedBytes = Uint8Array.from(atob(ENCRYPTED_BASE64), c => c.charCodeAt(0));
  const iv = encryptedBytes.slice(0, 12);
  const ciphertext = encryptedBytes.slice(12);

  const encoder = new TextEncoder();
  const keyData = encoder.encode(keyText);
  const key = await crypto.subtle.importKey(
    "raw",
    keyData,
    { name: "AES-GCM" },
    false,
    ["decrypt"]
  );

  const decryptedBuffer = await crypto.subtle.decrypt(
    { name: "AES-GCM", iv },
    key,
    ciphertext
  );

  return new TextDecoder().decode(decryptedBuffer);
}

function getSetting(settings: ISettingRegistry.ISettings, key: string, default_value: string): string {
  try {
    const value = settings.get(key).composite;
    return typeof value === 'string' ? value : '';
  } catch (err) {
    console.warn(`Error reading setting "${key}":`, err);
    return default_value;
  }
}

function htmlTableToMarkdown(html: string): string {
    const parser = new DOMParser();
    const doc = parser.parseFromString(html, "text/html");

    const table = doc.querySelector("table");
    if (!table) {
        throw new Error("No <table> found in HTML");
    }

    const rows = Array.from(table.querySelectorAll("tr"));
    const extractText = (el: Element) =>
        el.textContent?.trim().replace(/\s+/g, " ") ?? "";

    const mdRows = rows.map(row => {
        const cells = Array.from(row.children).map(extractText);
        return `| ${cells.join(" | ")} |`;
    });

    const firstRow = rows[0];
    const hasHeader = firstRow.querySelector("th") !== null;

    if (hasHeader) {
        const headerCellCount = firstRow.children.length;
        const separator = `| ${Array(headerCellCount).fill("---").join(" | ")} |`;
        mdRows.splice(1, 0, separator);
    }

    return mdRows.join("\n");
}

const plugin: JupyterFrontEndPlugin<void> = {
  id: 'm269-25j-marking-tool:plugin',
  description: 'A tutor marking tool for M269 in the 25J presentation',
  autoStart: true,
  requires: [ICommandPalette, INotebookTracker, ISettingRegistry, IDocumentManager],
  activate: async (
    app: JupyterFrontEnd, 
    palette: ICommandPalette, 
    notebookTracker: INotebookTracker, 
    settingRegistry: ISettingRegistry,
    docManager: IDocumentManager
  ) => {
    console.log('JupyterLab extension m269-25j-marking-tool is activated! hurrah');
    console.log('Loading settings registry');
    const settings = await settingRegistry.load('m269-25j-marking-tool:plugin');
    console.log('Loading colours');
    const answer_colour = getSetting(settings,'answer_colour','rgb(255, 255, 204)');
    const feedback_colour = getSetting(settings,'feedback_colour','rgb(93, 163, 243)');
    const tutor_colour = getSetting(settings,'tutor_colour','rgb(249, 142, 142)');
    console.log('Answers: '+answer_colour);
    console.log('Feedback: '+feedback_colour);
    console.log('Tutor: '+tutor_colour);
    // Inject custom styles
    const style = document.createElement('style');
    /*style.textContent = `
      .m269-answer {
        background-color:rgb(255, 255, 204) !important;
      }
      .m269-feedback {
        background-color:rgb(93, 163, 243) !important;
      }
      .m269-tutor {
        background-color: rgb(249, 142, 142) !important;
      }
    `;*/
    style.textContent = `
      .m269-answer {
        background-color:`+answer_colour+` !important;
      }
      .m269-feedback {
        background-color:`+feedback_colour+` !important;
      }
      .m269-tutor {
        background-color: `+tutor_colour+` !important;
      }
    `;
    document.head.appendChild(style);

    // Prep command
    app.commands.addCommand(prep_command, {
      label: 'M269 Prep for Marking',
      caption: 'M269 Prep for Marking',
      execute: async (args: any) => {
        const currentWidget = app.shell.currentWidget;
        if (currentWidget instanceof NotebookPanel) {
          const notebook = currentWidget.content;
          const metadata = currentWidget?.context?.model?.metadata;
          console.log('metadata');
          console.log(metadata);
          console.log(metadata["TMANUMBER"]);
          if (!metadata) {
            console.error('Notebook metadata is undefined');
            return;
          }
          if (metadata["TMANUMBER"] != 1 && metadata["TMANUMBER"] != 2 && metadata["TMANUMBER"] != 3) {
            alert("Could not identify TMA number.");
            return;
          }
          if (metadata["TMAPRES"] != "25J") {
            alert("This tool is only for presentation 25J. This TMA not identifiable as a 25J assessment.");
            return;
          }
          // Duplicate the file
          const oldName = currentWidget.context.path;
          const newName = oldName.replace(/\.ipynb$/, '-UNMARKED.ipynb');
          await app.serviceManager.contents.copy(oldName, newName);
          console.log('Notebook copied successfully:', newName);
          // Insert initial code cell
          notebook.activeCellIndex = 0;
          notebook.activate();
          await app.commands.execute('notebook:insert-cell-above');
          const cell = notebook.activeCell;
          console.log("Getting TMA number");
          if (cell && cell.model.type === 'code') {
            let question_marks = "";
            if (metadata["TMANUMBER"] == 1) {
              question_marks = question_marks_tma01;
            } else if (metadata["TMANUMBER"] == 2) {
              question_marks = question_marks_tma02;
            } else if (metadata["TMANUMBER"] == 3) {
              question_marks = question_marks_tma03;
            } else {
              alert("TMA Not identified from metadata");
              return;
            }
            (cell as CodeCell).model.sharedModel.setSource(`${initial_code_cell_pt1}\n\n${question_marks}\n\n${initial_code_cell_pt2}`);
            cell.model.setMetadata('CELLTYPE','MARKCODE');
            await app.commands.execute('notebook:run-cell');
            if (cell) {
              cell.inputHidden = true;
            }
          }
          console.log("inserting marking forms");
          // Insert marking cell after every cell with metadata "QUESTION"
          for (let i = 0; i < notebook.widgets.length; i++) {
            console.log(i);
            const currentCell = notebook.widgets[i];
            const meta = currentCell.model.metadata as any;
            const celltype = meta['CELLTYPE'];
            console.log(celltype);
            const questionValue = meta['QUESTION'];
            console.log(questionValue);
            if (celltype == 'TMACODE') {
              notebook.activeCellIndex = i;
              await app.commands.execute('notebook:run-cell');
            }
            if (questionValue !== undefined) {
              notebook.activeCellIndex = i;
              await app.commands.execute('notebook:insert-cell-below');
              let insertedCell = notebook.activeCell;
              if (insertedCell && insertedCell.model.type === 'code') {
                (insertedCell as CodeCell).model.sharedModel.setSource(`# Marking Form
generate_radio_buttons(${JSON.stringify(questionValue)})`);
                insertedCell.model.setMetadata('CELLTYPE','MARKCODE');
              }
              await app.commands.execute('notebook:run-cell');
              i++; // Skip over inserted cell to avoid infinite loop
              
              notebook.activeCellIndex = i;
              await app.commands.execute('notebook:insert-cell-below');
              await app.commands.execute('notebook:change-cell-to-markdown');
              insertedCell = notebook.activeCell;
              if (insertedCell && insertedCell.model.type === 'markdown') {
                console.log('markdown cell being metadatad');
                (insertedCell as CodeCell).model.sharedModel.setSource(`Feedback:`);
                insertedCell.model.setMetadata('CELLTYPE','FEEDBACK');
              } else {
                console.log('markdown cell cannot be metadatad');
              }
              await app.commands.execute('notebook:run-cell');
              i++; // Skip over inserted cell to avoid infinite loop
            }
          }
          // Insert final code cell at bottom
          //await app.commands.execute('notebook:activate-next-cell');
          notebook.activeCellIndex = notebook.widgets.length -1;

          console.log('Inserting final cell');
          await app.commands.execute('notebook:insert-cell-below');
          console.log('Getting final cell');
          const finalCell = notebook.widgets[notebook.widgets.length - 1];
          console.log(finalCell);
          if (finalCell) {
            console.log('Got final cell');
            console.log(finalCell.model.type);
          } else {
            console.log('Not got final cell');
          }
          if (finalCell && finalCell.model.type === 'code') {
            console.log('got and it is code');
            (finalCell as CodeCell).model.sharedModel.setSource(`create_summary_table()`);
            finalCell.model.setMetadata('CELLTYPE','MARKCODE');

          } else {
            console.log('could not get or not code');
          }
          console.log('activating');
          await app.commands.execute('notebook:run-cell');
          // Automatically run the colourise command after prep
          await app.commands.execute(colourise_command);
          console.log('done');
        }
      }
    });
    // End prep command

    // Finish command
    app.commands.addCommand(finish_marking, {
      label: 'M269 Finish Marking',
      caption: 'M269 Finish Marking',
      execute: async (args: any) => {
        let currentWidget = app.shell.currentWidget;
        if (currentWidget instanceof NotebookPanel) {
          let context = docManager.contextForWidget(currentWidget);
          if (!context) {
            console.warn("Not a document widget");
            return;
          }
          await context.save();
          const content = await context.model.toJSON();

          const oldPath = context.path;
          const newPath = oldPath.replace(/\.ipynb$/, '') + '-MARKED.ipynb';

          await docManager.services.contents.save(newPath, {
            type: 'notebook',
            format: 'json',
            content
          });

          await app.commands.execute('docmanager:open', { path: newPath });
          console.log('Regetting notebook.')
          // Wait until the widget tracker registers the new path
          let widget: NotebookPanel | null = null;
          for (let i = 0; i < 50; i++) {   // retry ~50 times over 1s
            widget = docManager.findWidget(newPath, 'Notebook') as NotebookPanel;
            console.log(i);
            if (widget) break;
            await new Promise(r => setTimeout(r, 20));
          }

          widget = docManager.findWidget(newPath, 'Notebook') as NotebookPanel;
          if (!widget) {
            console.error('Could not find new widget');
            return;
          }

          await widget.context.ready;

          currentWidget = widget

          //currentWidget = app.shell.currentWidget;
          
          if (currentWidget instanceof NotebookPanel) {
            context = docManager.contextForWidget(currentWidget);
          } else {
            console.log('Could not get new context');
            return;
          }
          
          const notebook = currentWidget.content;
          const metadata = currentWidget?.context?.model?.metadata;
          console.log('metadata');
          console.log(metadata);
          console.log(metadata["TMANUMBER"]);
          if (!metadata) {
            console.error('Notebook metadata is undefined');
            return;
          }
          if (metadata["TMANUMBER"] != 1 && metadata["TMANUMBER"] != 2 && metadata["TMANUMBER"] != 3) {
            alert("Could not identify TMA number.");
            return;
          }
          if (metadata["TMAPRES"] != "25J") {
            alert("This tool is only for presentation 25J. This TMA not identifiable as a 25J assessment.");
            return;
          }
          // Run mark code cells
          for (let i = 0; i < notebook.widgets.length; i++) {
              const currentCell = notebook.widgets[i];
              const meta = currentCell.model.metadata as any;
              const celltype = meta['CELLTYPE'];
            // console.log(celltype);
              if (celltype === "MARKCODE") {
                notebook.activeCellIndex = i;
                await app.commands.execute('notebook:run-cell');
              }
          }
          // Remove all marking cells
          for (let i = notebook.widgets.length-1; i >= 0;  i--) {
              const currentCell = notebook.widgets[i];
              const meta = currentCell.model.metadata as any;
              const celltype = meta['CELLTYPE'];
              if (celltype === "MARKCODE") {
                notebook.activeCellIndex = i;
                // Extract grade text
                //console.log('TEST');
                if (notebook.activeCell instanceof CodeCell) {
                  const outputs = notebook.activeCell.model.outputs;
                  let textOutput = '';
                  for (let i =0; i < outputs.length; i++) {
                    const out = outputs.get(i);
                    for (const mimeType of Object.keys(out.data)) {
                      if (mimeType === 'text/plain') {
                        const val = out.data[mimeType];
                        textOutput += Array.isArray(val) ? val.join('\n') : val;
                        textOutput += '\n';
                      }
                    }
                  }
                  //console.log(textOutput);
                  //const match = textOutput.match(/value='([^']+)'/);
                  //const grade = match ? match[1] : null;
                  const grade = extractRadioValueFromRepr(textOutput);
                  let html = null;
                  if (grade == null) {
                    console.log('possible iPython found')
                    if (notebook.activeCell instanceof CodeCell) {
                      const outputs = notebook.activeCell.model.outputs;
                      console.log(outputs);
                      for (let i = 0; i < outputs.length; i++) {
                        const out = outputs.get(i);
                        html = (out as any).data?.['text/html'];
                        if (typeof html === 'string') {
                            console.log(html);
                        }
                      }
                    }
                  }
                  console.log(grade);
                  console.log(1);
                  const active = notebook.activeCell;
                  // Put grade text in cell
                  if (active && active instanceof CodeCell){//} && grade != null) {
                    console.log(1.1);
                    await app.commands.execute('notebook:change-cell-to-markdown');
                    console.log(1.2);
                  }
                  console.log(2);
                  const updated = notebook.activeCell;
                  console.log(3);
                  if (updated && updated instanceof MarkdownCell) {
                    console.log(4);
                    if (grade == null && html != null) {
                      console.log(5);
                      console.log("-->"+html+"<--");
                      console.log(5.5);
                      //(updated as MarkdownCell).model.sharedModel.setSource("Six Seven");
                      const mdTable = htmlTableToMarkdown(html);
                      (updated as MarkdownCell).model.sharedModel.setSource(mdTable);
                      await app.commands.execute('notebook:run-cell');                      
                    } else {
                      if (grade == null) {
                        await app.commands.execute('notebook:delete-cell');
                      } else {
                        console.log(6);
                        (updated as MarkdownCell).model.sharedModel.setSource("Grade awarded: "+grade);
                      }
                    }
                  }
                }
              } else {
                // al_tests.py
                if (i == 0) {
                  notebook.activeCellIndex = i;
                  if (notebook.activeCell instanceof CodeCell) {
                    let existing = (currentCell as CodeCell).model.sharedModel.getSource();
                    if (existing.endsWith('al_tests.py')) {
                        await app.commands.execute('notebook:delete-cell');
                    }
                  }
                }
              }
          }      
        }
      }
    });
    // End finish command

    // Colourise command
    app.commands.addCommand(colourise_command, {
      label: 'M269 Colourise',
      caption: 'M269 Colourise',
      execute: async (args: any) => {
        const currentWidget = app.shell.currentWidget;
        if (currentWidget instanceof NotebookPanel) {
          const notebook = currentWidget.content;
          console.log('Colourising cells');
          for (let i = 0; i < notebook.widgets.length; i++) {
            console.log(i);
            const currentCell = notebook.widgets[i];
            const meta = currentCell.model.metadata as any;
            const celltype = meta['CELLTYPE'];
            console.log(celltype);
            if (celltype === 'ANSWER') {
              currentCell.addClass('m269-answer');
            } else if (celltype === "FEEDBACK") {
              currentCell.addClass('m269-feedback');
            } else if (celltype === "MARKCODE") {
              currentCell.addClass('m269-feedback');              
            } else if (celltype === "SOLUTION" || celltype === "SECREF" || celltype === "GRADING") {
              currentCell.addClass('m269-tutor');
            }
          }
        }
      }
    });
    // End colourise command

    // Prep-for-students command
    app.commands.addCommand(prep_for_students, {
      label: 'M269 Prep for Student (MT)',
      caption: 'M269 Prep for Student (MT)',
      execute: async (args: any) => {
        const currentWidget = app.shell.currentWidget;
        if (currentWidget instanceof NotebookPanel) {
          // Duplicate the file
          const oldName = currentWidget.context.path;
          const masterName = oldName;
          //const newName = oldName.replace(/-Master(?=\.ipynb$)/, "");
          const newName = oldName
            .replace(/-Master(?=\.ipynb$)/, "")
            .replace(/(?=\.ipynb$)/, "-STUDENT");

          await currentWidget.context.save();

          await app.serviceManager.contents.rename(oldName, newName);

          await currentWidget.close();
          
          const newWidget = await app.commands.execute('docmanager:open', {
            path: newName,
            factory: 'Notebook'
          });

          if (newWidget && 'context' in newWidget) {
            await (newWidget as NotebookPanel).context.ready;
          }
          
          await app.serviceManager.contents.copy(newName, masterName);
          
          console.log('Notebook copied successfully:', newName);
          // Iterate backwards over the cells
          const notebook = newWidget.content;
          for (let i = notebook.widgets.length - 1; i >= 0; i--) {
            const cell = notebook.widgets[i];
            const meta = cell.model.metadata as any;
            const celltype = meta['CELLTYPE'];
            // Do something with each cell
            console.log(`Cell ${i} type: ${cell.model.type} - ${celltype}`);
            if (celltype == 'SECREF' || celltype == 'SOLUTION' || celltype == 'GRADING') {
              notebook.activeCellIndex = i;
              await app.commands.execute('notebook:delete-cell');
              console.log('... deleted.');
            }
          }
        }
      }
    });

    async function ensurePopupsAllowed(): Promise<boolean> {
      // 1) Try to open a harmless placeholder immediately (sync).
      // If it returns null, the browser blocked it.
      const testWin = window.open('about:blank', '_blank');

      if (!testWin) {
        // 2) Build site/origin string for instructions
        //const baseUrl = PageConfig.getBaseUrl();          // e.g. "/user/olih/lab"
        const origin  = window.location.origin;           // e.g. "https://yourhub.example.org"
        //const site    = `${origin}${baseUrl}`.replace(/\/lab\/?$/, ''); // hub root-ish

        const body = document.createElement('div');
        body.innerHTML = `
          <p><b>Pop-ups are blocked</b> for <code>${origin}</code>. To open multiple notebooks automatically, please allow pop-ups for this site, then click <b>Try again</b>.</p>
          <details open>
            <summary><b>How to allow pop-ups</b></summary>
            <ul style="margin-top:0.5em">
              <li><b>Check your address bar:</b> There may be an option to whitelist popups.</li>
              <li><b>Chrome / Edge (Chromium):</b> Click the icon to left of address bar → <i>Site settings</i> → set <i>Pop-ups and redirects</i> to <b>Allow</b> for <code>${origin}</code>. Then close the tab to return.</li>
              <li><b>Firefox:</b> Preferences → <i>Privacy &amp; Security</i> → <i>Permissions</i> → uncheck <i>Block pop-up windows</i> or add an exception for <code>${origin}</code>.</li>
              <li><b>Safari (macOS):</b> Safari → Settings → <i>Websites</i> → <i>Pop-up Windows</i> → for <code>${origin}</code>, choose <b>Allow</b>. Or “Settings for This Website…” from the address bar.</li>
            </ul>
          </details>
          <p style="margin-top:0.5em">Tip: some extensions (ad blockers, privacy tools) also block pop-ups; whitelist this site there if needed.</p>
        `;
        const bodyWidget = new Widget({ node: body });

        const result = await showDialog({
          title: 'Allow pop-ups to open notebooks',
          body: bodyWidget,
          //buttons: [Dialog.cancelButton({ label: 'Cancel' }), Dialog.okButton({ label: 'Try again' })]
          buttons: [Dialog.cancelButton({ label: 'Cancel' })]
        });

        return result.button.accept;
      } else {
        // 3) We had permission—tidy up and continue
        try { testWin.close(); } catch { /* ignore */ }
        return true;
      }
    }

    // Prepare the AL tests command
    app.commands.addCommand(al_tests_command, {
      label: 'M269 AL Tests',
      caption: 'M269 AL Tests',
      
      execute: async (args: any) => {
        const contents = new ContentsManager();
        const currentWidget = notebookTracker.currentWidget;
        if (currentWidget) {
          const notebookPath = currentWidget.context.path; // e.g. "subdir/notebook.ipynb"
          console.log("Notebook path:", notebookPath);
        }
        const notebookPath = currentWidget?.context.path ?? ""
        const upLevels = notebookPath.split("/").length - 1;
        const relPathToRoot = Array(upLevels).fill("..").join("/");
        const fullPath = relPathToRoot ? `${relPathToRoot}/al_tests.py` : "al_tests.py";
        let fileContent: string;
        try {
          fileContent = await decrypt();
        } catch (err) {
          alert("Decryption failed: " + (err instanceof Error ? err.message : err));
          return;
        }
        //alert('here');
        const filePath = 'al_tests.py';  // This is in the root folder
        try {
          await contents.save(filePath, {
            type: 'file',
            format: 'text',
            content: fileContent
          });
          console.log('File created successfully');
          if (currentWidget instanceof NotebookPanel) {
            // 1. Put run call in cell 0
            const notebook = currentWidget.content;
            notebook.activeCellIndex = 0;
            notebook.activate();
            await app.commands.execute('notebook:insert-cell-above');
            const cell = notebook.activeCell;
            const code = `%run -i ${fullPath}`;
            (cell as CodeCell).model.sharedModel.setSource(code);
            await app.commands.execute('notebook:run-cell');
            // 2. Check TMA number
            const metadata = currentWidget?.context?.model?.metadata;
            console.log('metadata');
            console.log(metadata);
            console.log(metadata["TMANUMBER"]);
            if (!metadata) {
              console.error('Notebook metadata is undefined');
              return;
            }
            if (metadata["TMANUMBER"] != 1 && metadata["TMANUMBER"] != 2 && metadata["TMANUMBER"] != 3) {
              alert("Could not identify TMA number.");
              return;
            }
            if (metadata["TMAPRES"] != "25J") {
              alert("This tool is only for presentation 25J. This TMA not identifiable as a 25J assessment.");
              return;
            }
            console.log('Identified as TMA '+metadata["TMANUMBER"]+' Presentation '+metadata["TMAPRES"]);
            // 3. Iterate over dictionary for relevant TMA puttin calls in CELLTYPE:ANSWER with relevant QUESTION at last line.
            const tmaNumber = metadata["TMANUMBER"];
            const entries = testCalls[tmaNumber];
            if (entries) {
              for (const [key, value] of Object.entries(entries)) {
                console.log(`Key: ${key}, Value: ${value}`);
                for (let i = 0; i < notebook.widgets.length; i++) {
                  const currentCell = notebook.widgets[i];
                  const meta = currentCell.model.metadata as any;
                  const questionKey = meta["QUESTION"];
                  const cellType = meta["CELLTYPE"];
                  console.log(`Cell ${i}: Type = ${cellType}, Question = ${questionKey}`);
                  if (cellType === "ANSWER" && questionKey === key && currentCell.model.type === "code") {
                    console.log('found');
                    let existing = (currentCell as CodeCell).model.sharedModel.getSource();
                    (currentCell as CodeCell).model.sharedModel.setSource(existing + `\n\n`+value);
                  }
                  if (i == 18 || i == 19 || i == 20) {
                    console.log(cellType);
                    console.log(cellType === "ANSWER");
                    console.log(questionKey);
                    console.log(key)
                    console.log(questionKey === key);
                    console.log(currentCell.model.type)
                    console.log(currentCell.model.type === "code");
                  }
                }
              }
            }
            console.log(code);
          } else {
            alert('Error: Could not access NotebookPanel');
            return;
          }
        } catch (err) {
          alert('Failed to create file: '+ err);
          return;
        }
      }
    });

    // Open all TMAs
    app.commands.addCommand(open_all_tmas, {
            label: 'M269 Open All TMAs',
      caption: 'M269 Open All TMAs',
      
      execute: async (args: any) => {
        // Ask for popup permission (or instructions if blocked)
        const ok = await ensurePopupsAllowed();
        if (!ok) return; // user cancelled
        //alert('OK');
        const contents = app.serviceManager.contents;
        // 1) collect all notebooks from the Jupyter root
        let notebooks = await walkDir(contents, ''); // '' = root

        notebooks = notebooks.filter(path => !path.includes('-UNMARKED'));

        // DEBUG
        const baseUrl = PageConfig.getBaseUrl();
        console.log('OPEN ALL DEBUGGING START');
        for (const path of notebooks) {
          const url = baseUrl + 'lab/tree/' + encodeURIComponent(path);
          console.log('>> '+url);
        }
        console.log('OPEN ALL DEBUGGING END');


        // END DEBUG

        // (optional) sanity check so you don't open hundreds at once
        if (notebooks.length > 20) {
          const ok = window.confirm(
            `Found ${notebooks.length} notebooks. Open them all in new tabs?`
          );
          if (!ok) return;
        }
        
        // 2) open each notebook in a new browser tab
        //const baseUrl = PageConfig.getBaseUrl();
        for (const path of notebooks) {
          const url = baseUrl + 'lab/tree/' + encodeURIComponent(path);
          window.open(url, '_blank');
        }

        alert(`Opened ${notebooks.length} notebooks in new tabs.\mIf they didn't open, enable popups for this site and try again.`);   
      }
    });

    const category = 'M269-25j';
    // Add commands to pallette
    palette.addItem({ command: prep_command, category, args: { origin: 'from palette' } });
    palette.addItem({ command: colourise_command, category, args: { origin: 'from palette' } });
    palette.addItem({ command: prep_for_students, category, args: { origin: 'from palette' } });
    palette.addItem({ command: al_tests_command, category, args: {origin: 'from palette' }});
    palette.addItem({ command: open_all_tmas, category, args: {origin: 'from palette' }});
    palette.addItem({ command: finish_marking, category, args: {origin: 'from palette' }});
  }
};

export default plugin;
