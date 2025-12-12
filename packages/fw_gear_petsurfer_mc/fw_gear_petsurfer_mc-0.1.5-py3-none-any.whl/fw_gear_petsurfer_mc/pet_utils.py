"""Main module."""

import datetime
import logging
import os
import re
import shutil
import subprocess
from pathlib import Path

import nibabel as nib
import pandas as pd

import matplotlib.pyplot as plt
import seaborn as sns

pd.options.mode.chained_assignment = None

log = logging.getLogger(__name__)
log.setLevel("DEBUG")


def pet_get_images(ses, indir: str, regex: str = "Frame") -> list:
    """Get PET volumes in NIfTI format from a session."""
    # Get acquisition container info
    acq = ses.acquisitions.find()
    reg = re.compile(regex, re.IGNORECASE)

    if acq:
        nifti_files = []
        for i in range(len(acq)):
            for infile in acq[i].files:
                filename = Path(infile.get("name"))
                if reg.findall(filename.as_posix()):
                    if infile.type == "nifti":
                        pet_file = indir / filename
                        acq[i].download_file(filename.as_posix(), pet_file.as_posix())
                        log.info("%s downloaded ", Path(filename.as_posix()))
                        nifti_files.append(pet_file.as_posix())
                    else:
                        log.info("Wrong file type of %s  ", infile.get("name"))
                else:
                    log.info("No pattern %s found", regex)
    else:
        log.debug("Acquisition container can not be found or it's empty")

    return nifti_files


def rewrite_pet(out_dir, pet_files):
    """Cleaning filenames and rewrite nifti file in output dir."""
    # outdir = gear_context.output_dir.as_posix()
    new_pet_list = []
    for img in pet_files:
        orig_name = os.path.basename(img)
        new_name = "".join([out_dir, "/", re.sub(r"[\[\]]", "", orig_name)])
        try:
            shutil.copyfile(img, new_name)
        except shutil.SameFileError:
            pass
        new_pet_list.append(new_name)

    return new_pet_list


def append_file_tag(filename, tag):
    """Append a postfix tag in files with double extensions, such as *.nii.gz"""
    p0 = Path(filename)
    fp = Path(p0.stem)
    p = Path(fp)

    out_filename = p.stem + tag + p.suffix + p0.suffix
    return Path(out_filename)


def write_avg_pet(out_dir, pet_file):
    """
    Takes one image (pet_file) ad input and
    change the name appending '_avg' as postfix
    Args:
        out_dir: output directory where the image will be saved
        pet_file: single pet volume

    Returns: nifti volume with file name changed to append '_avg' as postfix

    """
    img = nib.load(pet_file[0])
    orig_name = os.path.basename(pet_file[0])
    avg_fname = append_file_tag(orig_name, "_avg")
    new_name = out_dir / avg_fname
    nib.save(img, new_name)
    log.info(f"{new_name} has been written.")

    return new_name


def merge_pet_frames(images, good_indices=None):
    """Stack a list of 3D images into 4D image."""
    if good_indices is None:
        good_indices = range(len(images))
    images = [img for i, img in enumerate(images) if i in good_indices]
    out_img = nib.concat_images(images)
    out_name = append_file_tag(images[0], "_merged")
    new_name = re.sub(r"[\[\]]", "", out_name.as_posix())
    new_name = re.sub(r"Frame_1_of_6_", "", new_name)

    filename = "".join([os.path.dirname(images[0]), "/", new_name])
    nib.save(out_img, filename)

    return out_img, filename


def get_nifti_format(nifti_file):
    """If only one nifti file is found, return nifti dim"""
    if isinstance(nifti_file, str):
        nifti_file = [nifti_file]

    if len(nifti_file) == 1:
        image = nib.load(nifti_file[0])
        return image.ndim
    else:
        log.info("Data include a serie of 3D frames.")
        return 0


def pet_mri_convert(pet_images, frameno, out_dir):
    """
    If your PET data only has one frame (eg, an uptake image), then that will be your template.
    If your PET data has multiple frames (ie, dynamic), then you will need to create the template from the dynamic data.
    This can be done by extracting a single frame: mri_convert pet.nii.gz --frame frameno template.nii.gz
    Args:
        pet_images:
        frameno: frame to take as reference
        out_dir: output directory

    Returns: template image (*avg.nii.gz)

    """

    begin_time = datetime.datetime.now()

    log.info(f"RUNNING: mri_convert {pet_images} --frame {frameno} template_avg.nii.gz")

    cmd = "".join([os.environ["FREESURFER_HOME"], "/", "bin/", "mri_convert"])
    cmd_torun = [
        cmd,
        pet_images,
        "--frame",
        frameno,
        Path(out_dir) / "template_avg.nii.gz",
    ]

    subprocess.run(cmd_torun)

    end_time = datetime.datetime.now() - begin_time
    log.info(f"end: {end_time}\n")

    return Path(out_dir) / "template_avg.nii.gz"


def pet_mri_concat(pet_images, out_dir):
    begin_time = datetime.datetime.now()

    log.info(f"RUNNING: mri_concat {pet_images} --mean --o template.nii.gz")

    cmd = "".join([os.environ["FREESURFER_HOME"], "/", "bin/", "mri_concat"])
    cmd_torun = [
        cmd,
        "--mean",
        pet_images[0],
        "--o",
        Path(out_dir) / "template_avg.nii.gz",
    ]

    subprocess.run(cmd_torun)

    end_time = datetime.datetime.now() - begin_time
    log.info(f"end: {end_time}\n")

    return Path(out_dir) / "template_avg.nii.gz"


def pet_template_creation(pet_images, frameno, out_dir, template_option="mean"):
    if template_option == "mean":
        template_avg = pet_mri_concat(pet_images, out_dir)
        return template_avg

    elif template_option == "frame" and frameno:
        template_avg = pet_mri_convert(pet_images, int(frameno), out_dir)
        return template_avg
    else:
        nii_dim = get_nifti_format(pet_images[0])
        log.error(
            f"These PET data include {nii_dim} frames. A frame number has to be specified for the template creation."
        )
        return -1


def pet_mc(out_dir: str, pet_files, temp):
    """[summary]

    Args:
        out_dir: output directory to save the motion corrected images
        pet_files: list of PET files to estimate the motion correction using mc-afni2
        temp: template image, that is the target for the motion correction estimation

    Returns:

          The AFNI 3dvolreg output mcdat file will have the following 10 columns:

          1. n      : time point
          2. roll   : rotation about the I-S axis (degrees CCW)
          3. pitch  : rotation about the R-L axis (degrees CCW)
          4. yaw    : rotation about the A-P axis (degrees CCW)
          5. dS     : displacement in the Superior direction (mm)
          6. dL     : displacement in the Left direction (mm)
          7. dP     : displacement in the Posterior direction (mm)
          8. rmsold : RMS difference between input frame and reference frame
          9. rmsnew : RMS difference between output frame and reference frame
          10. trans : translation (mm) = sqrt(dS^2 + dL^2 + dP^2)
    """
    log = logging.getLogger(__name__)
    log.setLevel("DEBUG")

    begin_time = datetime.datetime.now()

    mc_files = "".join(
        [
            out_dir,
            "/",
            os.path.basename(pet_files[0]).split(".")[0],
            "_avg",
            ".nii.gz",
        ]
    )
    dat_files = "".join(
        [
            out_dir,
            "/",
            os.path.basename(pet_files[0]).split(".")[0],
            "_avg",
            ".dat",
        ]
    )

    mc_afni_cmd = "".join(
        [os.environ["FREESURFER_HOME"], "/", "fsfast/", "bin/", "mc-afni2"]
    )

    cmd_torun = [
        mc_afni_cmd,
        "--i",
        pet_files[0],
        "--t",
        temp,
        "--o",
        re.sub("avg", "mc", mc_files),
        "--mcdat",
        re.sub("avg", "mc", dat_files),
    ]

    subprocess.run(cmd_torun)

    end_time = datetime.datetime.now() - begin_time
    # Write on subject log files
    log.info(f"end: {end_time}\n")

    return 0


def determine_plot_label(plotname: str):
    """

    Args:
        plotname: Only two options allowed: rotation or displacement

    Returns: ylabel of the plot

    """
    if plotname == "rotation":
        ylab = "Rotation [CCW]"
    elif plotname == "displacement":
        ylab = "Displacement [mm]"
    else:
        log.debug("Only two options allowed: rotation or displacement")
        return None, None
    return "Time Points", ylab


def make_mcplot(outdir: str, df, plotname: str):
    # remove first column if dim > 9
    if df.shape[1] > 9:
        df = df.iloc[:, 1:]

    df.columns = ["roll", "pitch", "yaw", "dS", "dL", "dP", "rmsold", "rmsnew", "trans"]
    # Save rotations params
    if plotname == "rotation":
        df_rot = df[["roll", "pitch", "yaw"]]
    elif plotname == "displacement":
        df_rot = df[["dS", "dL", "dP"]]
    else:
        log.debug("Only two optinos allowed: rotation or displacement")

    df_rot["time_points"] = list(df_rot.index + 1)
    dfm = df_rot.melt("time_points", var_name="cols", value_name="vals")
    g = sns.catplot(
        x="time_points", y="vals", hue="cols", data=dfm, kind="point", legend=False
    )

    xlabel, ylabel = determine_plot_label(plotname)
    g.set(xlabel=xlabel, ylabel=ylabel)
    plt.legend(title="MC Params", loc="upper left")
    outfile = f"{outdir}/mc_{plotname}.png"
    plt.savefig(outfile)
    log.info("%s saved", outfile)


def plot_and_write_mc_params_from_dat(outdir: Path):
    """Read dat file to report mc rotation and translation as metadata"""
    dat_files = list(outdir.glob("*_mc.dat"))
    mc_parameters = {}

    if len(dat_files) > 1:
        sorted_dat_files = sorted(dat_files, key=lambda x: int(x.name.split("_")[-1]))
        meta_dat = {}
        for dat in sorted_dat_files:
            with open(dat, "r") as file:
                text = file.read().splitlines()
                meta_dat[dat.name] = text
        mc_parameters = {"mc_params": meta_dat}
    elif len(dat_files) == 1:
        df_data = pd.read_csv(dat_files[0], delimiter=r"\s+", header=None)
        df_data = df_data.rename_axis(None)

        make_mcplot(outdir, df_data, plotname="rotation")
        make_mcplot(outdir, df_data, plotname="displacement")

        df_data = df_data.set_axis(
            ["n", "roll", "pith", "yaw", "dS", "dL", "dP", "rmsold", "rmsnew", "tans"],
            axis=1,
        )
        df_data = df_data.drop("n", axis=1)
        mc_parameters = {
            "mc_params": df_data.to_dict(),
            "variance": df_data.var().to_dict(),
        }

    return mc_parameters
